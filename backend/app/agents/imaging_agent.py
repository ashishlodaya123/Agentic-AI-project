import os
from PIL import Image
import json

class MedicalImagingAgent:
    """
    Agent to analyze medical images using rule-based logic for demonstration purposes.
    In a production environment, this would integrate with specialized medical imaging models.
    """
    def __init__(self):
        pass

    def run(self, image_path: str) -> dict:
        """
        Analyzes an image and returns a structured classification.
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return {
                    "status": "error",
                    "message": "Image file not found.",
                    "analysis": None
                }
                
            # Get basic image information
            image = Image.open(image_path)
            width, height = image.size
            mode = image.mode
            
            # Simple rule-based analysis
            analysis = self._analyze_image_properties(width, height, mode, image_path)
            return {
                "status": "success",
                "message": "Image analysis completed successfully.",
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing image: {str(e)}",
                "analysis": None
            }

    def _analyze_image_properties(self, width: int, height: int, mode: str, image_path: str) -> dict:
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
            "file_size": f"{file_size:.1f} KB",
            "observations": observations,
            "recommendations": recommendations + specialty_recommendations,
            "technical_quality": "Adequate" if width > 300 and height > 300 else "Suboptimal"
        }