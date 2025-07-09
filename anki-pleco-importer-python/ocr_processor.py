#!/usr/bin/env python3
"""
OCR processor for Pleco dictionary screenshots using Azure Computer Vision API.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

import requests

try:
    import easyocr

    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("EasyOCR not available. Install with: pip install easyocr")

try:
    import pytesseract
    from PIL import Image

    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Tesseract not available. Install with: pip install pytesseract pillow")


class AzureOCRProcessor:
    """Process images using Azure Computer Vision OCR API."""

    def __init__(self, subscription_key: str, endpoint: str):
        """Initialize with Azure credentials."""
        self.subscription_key = subscription_key
        self.endpoint = endpoint
        self.ocr_url = f"{endpoint}/vision/v3.2/read/analyze"

    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process a single image and return OCR results."""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/octet-stream",
        }

        # Read image file
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Submit image for OCR
        response = requests.post(self.ocr_url, headers=headers, data=image_data)
        response.raise_for_status()

        # Get operation location from response headers
        operation_location = response.headers["Operation-Location"]

        # Poll for results
        while True:
            get_response = requests.get(
                operation_location,
                headers={"Ocp-Apim-Subscription-Key": self.subscription_key},
            )
            get_response.raise_for_status()
            result = get_response.json()

            if result["status"] == "succeeded":
                return result
            elif result["status"] == "failed":
                raise Exception(f"OCR failed: {result}")

            # Wait before polling again
            time.sleep(1)

    def extract_text_lines(self, ocr_result: Dict[str, Any]) -> List[str]:
        """Extract text lines from OCR result."""
        lines = []
        if "analyzeResult" in ocr_result:
            for page in ocr_result["analyzeResult"]["readResults"]:
                for line in page["lines"]:
                    lines.append(line["text"])
        return lines

    def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """Process all images in a directory."""
        directory = Path(directory_path)
        results = {}

        for image_file in directory.glob("*.png"):
            print(f"Processing {image_file.name}...")
            try:
                ocr_result = self.process_image(str(image_file))
                text_lines = self.extract_text_lines(ocr_result)

                results[image_file.name] = {
                    "file_path": str(image_file),
                    "text_lines": text_lines,
                    "full_ocr_result": ocr_result,
                    "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Save individual JSON file
                json_path = image_file.with_suffix(".json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(results[image_file.name], f, ensure_ascii=False, indent=2)

                print(f"  Extracted {len(text_lines)} lines of text")

            except Exception as e:
                print(f"  Error processing {image_file.name}: {e}")
                results[image_file.name] = {
                    "file_path": str(image_file),
                    "error": str(e),
                    "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }

        return results


def main():
    """Main function to process images."""
    # Use environment variables for Azure credentials
    subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    
    if not subscription_key or not endpoint:
        print("Error: Please set AZURE_SUBSCRIPTION_KEY and AZURE_ENDPOINT environment variables")
        sys.exit(1)

    # Process images in the specified directory
    images_dir = "features/examples/images"
    processor = AzureOCRProcessor(subscription_key, endpoint)

    try:
        results = processor.process_directory(images_dir)

        # Save combined results
        combined_results_path = Path(images_dir) / "ocr_results.json"
        with open(combined_results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\nProcessed {len(results)} images")
        print(f"Combined results saved to {combined_results_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
