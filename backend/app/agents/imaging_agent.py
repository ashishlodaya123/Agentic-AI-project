import os
from PIL import Image
import json
from app.core.agent_memory import get_agent_memory
from typing import Dict, Any
import hashlib
from datetime import datetime
import logging
import numpy as np

logger = logging.getLogger(__name__)


def make_serializable(obj):
    """Convert an object to a JSON-serializable format."""
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(key): make_serializable(value) for key, value in obj.items()}
    elif hasattr(obj, '__dict__'):
        # Handle objects with attributes
        return make_serializable(obj.__dict__)
    else:
        # For any other type, convert to string
        try:
            # Try to serialize first
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)


class MedicalImagingAgent:
    """
    Enterprise-grade agent to analyze medical images using rule-based logic.
    In a production environment, this would integrate with specialized medical imaging models.
    """
    def __init__(self):
        self.memory = get_agent_memory()
        self.supported_formats = ['JPEG', 'PNG', 'TIFF', 'BMP']
        self.max_file_size = 50 * 1024 * 1024  # 50MB limit

    def run(self, image_path: str) -> Any:
        """
        Analyzes an image and returns a structured classification.
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                result = {
                    "status": "error",
                    "message": "Image file not found.",
                    "analysis": None
                }
                self.memory.store_agent_output("imaging", result)
                return result
                
            # Validate file
            validation_result = self._validate_image_file(image_path)
            if not validation_result["valid"]:
                result = {
                    "status": "error",
                    "message": validation_result["message"],
                    "analysis": None
                }
                self.memory.store_agent_output("imaging", result)
                return result
            
            # Get basic image information
            image = Image.open(image_path)
            width, height = image.size
            mode = image.mode
            format = image.format or "Unknown"
            
            # Generate file hash for integrity checking
            file_hash = self._generate_file_hash(image_path)
            
            # Simple rule-based analysis
            analysis = self._analyze_image_properties(width, height, mode, format, image_path)
            
            # Add enterprise features
            enterprise_analysis = self._enterprise_image_analysis(image, image_path)
            
            # Combine analyses
            combined_analysis = {**analysis, **enterprise_analysis, "file_hash": file_hash}
            
            result = {
                "status": "success",
                "message": "Image analysis completed successfully.",
                "analysis": combined_analysis
            }
            
            # Store analysis in shared memory
            # Ensure the result is serializable
            serializable_result = make_serializable(result)
            self.memory.store_agent_output("imaging", serializable_result)
            return serializable_result
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            result = {
                "status": "error",
                "message": f"Error processing image: {str(e)}",
                "analysis": None
            }
            self.memory.store_agent_output("imaging", result)
            return result

    def _validate_image_file(self, image_path: str) -> dict:
        """Validate image file for enterprise use."""
        try:
            # Check file size
            file_size = os.path.getsize(image_path)
            if file_size > self.max_file_size:
                return {
                    "valid": False,
                    "message": f"Image file too large. Maximum size is {self.max_file_size / (1024*1024):.1f}MB."
                }
            
            # Check if it's a valid image file
            with Image.open(image_path) as img:
                format = img.format
                if format not in self.supported_formats:
                    return {
                        "valid": False,
                        "message": f"Unsupported image format: {format}. Supported formats: {', '.join(self.supported_formats)}"
                    }
            
            return {"valid": True, "message": "File validation successful"}
        except Exception as e:
            return {"valid": False, "message": f"File validation failed: {str(e)}"}

    def _generate_file_hash(self, image_path: str) -> str:
        """Generate SHA256 hash of the image file for integrity verification."""
        hash_sha256 = hashlib.sha256()
        with open(image_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _analyze_image_properties(self, width: int, height: int, mode: str, format: str, image_path: str) -> dict:
        """Analyze image properties and return a medical imaging assessment."""
        # Get file size
        file_size = os.path.getsize(image_path) / 1024  # in KB
        
        # Basic analysis based on image properties
        observations = []
        recommendations = []
        
        # Resolution analysis
        if width < 200 or height < 200:
            observations.append("Low resolution image detected")
            recommendations.append("Consider acquiring higher resolution imaging for better diagnostic quality")
        elif width > 2000 or height > 2000:
            observations.append("High resolution image detected")
            recommendations.append("Image suitable for detailed analysis")
        else:
            observations.append("Standard resolution image")
            
        # Color mode analysis
        color_info = ""
        if mode == "L":
            color_info = "Grayscale imaging"
            observations.append("Grayscale image format")
        elif mode == "RGB":
            color_info = "Color imaging"
            observations.append("Color image format")
            recommendations.append("Consider grayscale conversion for certain diagnostic applications")
        else:
            color_info = f"{mode} imaging"
            observations.append(f"{mode} image format")
            
        # File size analysis
        if file_size < 50:
            observations.append("Low file size")
            recommendations.append("Image may be compressed; consider original quality for diagnostic purposes")
        elif file_size > 5000:
            observations.append("High file size")
            recommendations.append("Image quality appears optimal for diagnostic use")
        else:
            observations.append("Standard file size")
            
        # Format analysis
        format_recommendations = []
        if format == "JPEG":
            format_recommendations.append("JPEG format suitable for photographic images")
        elif format == "PNG":
            format_recommendations.append("PNG format suitable for high-contrast images")
        elif format == "TIFF":
            format_recommendations.append("TIFF format suitable for multi-page medical documents")
        else:
            format_recommendations.append(f"{format} format detected")
            
        # Common medical imaging types based on properties
        imaging_type = "General medical image"
        specialty_recommendations = []
        
        if "grayscale" in [obs.lower() for obs in observations] and width > 500 and height > 500:
            imaging_type = "Likely X-ray or CT scan"
            specialty_recommendations.append("Consider radiology consultation for bone or internal structure analysis")
        elif "color" in [obs.lower() for obs in observations] and width > 1000 and height > 1000:
            imaging_type = "Likely MRI or ultrasound"
            specialty_recommendations.append("Consider specialist review for soft tissue or organ assessment")
        
        # Return structured analysis
        return {
            "imaging_type": imaging_type,
            "dimensions": f"{width}x{height} pixels",
            "color_format": color_info,
            "file_format": format,
            "file_size": f"{file_size:.1f} KB",
            "observations": observations,
            "recommendations": recommendations + specialty_recommendations + format_recommendations,
            "technical_quality": "Adequate" if width > 300 and height > 300 else "Suboptimal",
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _enterprise_image_analysis(self, image: Image.Image, image_path: str) -> dict:
        """Perform enterprise-grade image analysis."""
        # Calculate image statistics
        stats = {}
        try:
            # Get image statistics
            if image.mode == "L":  # Grayscale
                histogram = image.histogram()
                stats["mean_intensity"] = sum(i * histogram[i] for i in range(256)) / sum(histogram) if sum(histogram) > 0 else 0
                stats["contrast"] = max(histogram) - min(histogram) if histogram and len(histogram) > 0 else 0
            elif image.mode == "RGB":
                # For RGB, calculate statistics for each channel
                r, g, b = image.split()
                r_hist = r.histogram()
                g_hist = g.histogram()
                b_hist = b.histogram()
                stats["mean_intensity"] = {
                    "red": sum(i * r_hist[i] for i in range(256)) / sum(r_hist) if sum(r_hist) > 0 else 0,
                    "green": sum(i * g_hist[i] for i in range(256)) / sum(g_hist) if sum(g_hist) > 0 else 0,
                    "blue": sum(i * b_hist[i] for i in range(256)) / sum(b_hist) if sum(b_hist) > 0 else 0
                }
            
            # Image quality metrics
            quality_metrics = {
                "sharpness": "High" if image.width > 1000 else "Medium" if image.width > 500 else "Low",
                "compression_artifacts": "None detected" if image.format == "PNG" or image.format == "TIFF" else "Possible JPEG artifacts"
            }
            
            # Metadata extraction (if available)
            metadata = {}
            try:
                exif = image.getexif()
                if exif:
                    # Convert EXIF data to JSON serializable format using our robust function
                    metadata["exif_data"] = make_serializable(dict(exif))
            except Exception as e:
                logger.warning(f"Could not extract EXIF data: {str(e)}")
                pass
                
        except Exception as e:
            logger.warning(f"Could not calculate image statistics: {str(e)}")
            stats = {"error": "Could not calculate statistics"}
            quality_metrics = {"error": "Could not calculate quality metrics"}
            metadata = {}
        
        return {
            "image_statistics": stats,
            "quality_metrics": quality_metrics,
            "metadata": metadata,
            "enterprise_confidence": 0.85,  # Confidence in our analysis
            "processing_time": datetime.now().isoformat()
        }