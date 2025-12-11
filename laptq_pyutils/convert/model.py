from laptq_pyutils.log import load_logger


LOGGER = load_logger()


def convert_onnx_to_tensorrt(**kwargs):
    import os
    import tensorrt as trt

    path__file__input = kwargs["path__file__input"]
    path__file__output = kwargs["path__file__output"]
    precision = kwargs["precision"]
    dynamic_shape = kwargs["dynamic_shape"]
    max_workspace_size = kwargs["max_workspace_size"]  # GiB

    assert precision in ["fp32", "fp16"]

    logger_trt = trt.Logger(trt.Logger.WARNING)  # Use VERBOSE for detailed logs
    builder = trt.Builder(logger_trt)

    # Create a network with explicit batch mode
    network = builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    )

    # Check for int8/fp16 support
    if precision == "int8" and not builder.platform_has_fast_int8:
        raise RuntimeError("int8 not supported on this platform")

    parser = trt.OnnxParser(network, logger_trt)

    # Parse the ONNX model
    with open(path__file__input, "rb") as model:
        if not parser.parse(model.read()):
            for error in range(parser.num_errors):
                LOGGER.error(parser.get_error(error))
            raise RuntimeError("ERROR: Failed to parse the ONNX file.")

    # Create builder configuration
    config = builder.create_builder_config()
    config.set_tactic_sources(1 << int(trt.TacticSource.CUBLAS))
    config.set_memory_pool_limit(
        trt.MemoryPoolType.WORKSPACE, max_workspace_size * (1 << 30)
    )  # Set workspace size

    # Enable mixed precision if supported
    if builder.platform_has_fast_fp16 and precision == "fp16":
        config.set_flag(trt.BuilderFlag.FP16)
    elif builder.platform_has_fast_int8 and precision == "int8":
        config.set_flag(trt.BuilderFlag.INT8)
        raise Exception("int8 calibration is not implemented yet!")

    # Add dynamic shape optimization profile if enabled
    if dynamic_shape is not None:
        profile = builder.create_optimization_profile()
        for i in range(network.num_inputs):
            tensor = network.get_input(i)
            input_name = tensor.name
            input_shape = dynamic_shape.get(input_name)
            if input_shape:
                profile.set_shape(
                    input_name,
                    input_shape[0],  # Minimum shape
                    input_shape[1],  # Optimal shape
                    input_shape[2],  # Maximum shape
                )
            else:
                LOGGER.warning(f"Input '{input_name}' exists in network but no dynamic_shape config provided. It will be static.")
        config.add_optimization_profile(profile)

    # Build the engine
    serialized_engine = builder.build_serialized_network(network, config)
    if serialized_engine is None:
        raise RuntimeError("Failed to build the serialized TensorRT engine")

    # Deserialize the serialized engine
    runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
    engine = runtime.deserialize_cuda_engine(serialized_engine)
    if engine is None:
        raise RuntimeError("Failed to build the TensorRT engine")

    # Serialize and save the engine
    os.makedirs(os.path.dirname(path__file__output), exist_ok=True)
    with open(path__file__output, "wb") as file:
        file.write(engine.serialize())
    LOGGER.success("TensorRT engine is saved at: {}".format(path__file__output))
