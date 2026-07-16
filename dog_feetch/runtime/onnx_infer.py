#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import onnxruntime


class OnnxInfer:
    def __init__(self, onnx_model_path, input_name="obs", awd=False):
        """
        This module wraps ONNX Runtime policy inference.
        This module wraps ONNX Runtime policy inference.
        This module wraps ONNX Runtime policy inference.
        This module wraps ONNX Runtime policy inference.
        """
        self.onnx_model_path = onnx_model_path

        # ==========================================
        # This module wraps ONNX Runtime policy inference.
        # ==========================================
        # This module wraps ONNX Runtime policy inference.
        self.ort_session = onnxruntime.InferenceSession(
            self.onnx_model_path, providers=["CPUExecutionProvider"]
        )
        self.input_name = input_name
        self.awd = awd

    def infer(self, inputs):
        """
        This module wraps ONNX Runtime policy inference.
        This module wraps ONNX Runtime policy inference.
        This module wraps ONNX Runtime policy inference.
        """
        if self.awd:
            # ==========================================
            # This module wraps ONNX Runtime policy inference.
            # ==========================================
            # This module wraps ONNX Runtime policy inference.
            # This module wraps ONNX Runtime policy inference.
            outputs = self.ort_session.run(None, {self.input_name: [inputs]})

            # This module wraps ONNX Runtime policy inference.
            return outputs[0][0]
        else:
            # ==========================================
            # This module wraps ONNX Runtime policy inference.
            # ==========================================
            # This module wraps ONNX Runtime policy inference.
            outputs = self.ort_session.run(
                None, {self.input_name: inputs.astype("float32")}
            )
            # This module wraps ONNX Runtime policy inference.
            return outputs[0]


if __name__ == "__main__":
    import argparse
    import numpy as np
    import time

    # ==========================================
    # This module wraps ONNX Runtime policy inference.
    # ==========================================
    parser = argparse.ArgumentParser(description="ONNX ")
    parser.add_argument("-o", "--onnx_model_path", type=str, required=True, help="ONNX ")
    args = parser.parse_args()

    # This module wraps ONNX Runtime policy inference.
    oi = OnnxInfer(args.onnx_model_path, awd=True)

    # This module wraps ONNX Runtime policy inference.
    # This module wraps ONNX Runtime policy inference.
    inputs = np.random.uniform(size=54).astype(np.float32)
    # This module wraps ONNX Runtime policy inference.
    inputs = np.arange(47).astype(np.float32)

    times = []

    # ==========================================
    # This module wraps ONNX Runtime policy inference.
    # ==========================================
    print(" 1000 ...")
    for i in range(1000):
        start = time.time()

        # This module wraps ONNX Runtime policy inference.
        print(oi.infer(inputs))

        # This module wraps ONNX Runtime policy inference.
        times.append(time.time() - start)

    # ==========================================
    # This module wraps ONNX Runtime policy inference.
    # ==========================================
    avg_time = sum(times) / len(times)
    print("\n" + "="*40)
    print(f" (Average time): {avg_time * 1000:.3f} ms")
    print(f" (Average FPS) : {1 / avg_time:.1f} Hz")
    print("="*40)
