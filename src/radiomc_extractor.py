from typing import Dict
import SimpleITK as sitk
import numpy as np
from scipy.stats import gmean
from radiomics import featureextractor


class RadiomicExtractor:
    def apply_window(self, image, level, width):
        min_intensity = level - width / 2
        max_intensity = level + width / 2

        return sitk.Clamp(image, lowerBound=min_intensity, upperBound=max_intensity)

    def extract_features(self, image_path:str, mask_path:str) -> Dict[str, float]:
        image = sitk.ReadImage(image_path)
        image = apply_window(image, 40, 400)
    
        mask = sitk.ReadImage(mask_path)

        settings = {
            'binWidth': 25,
            'normalize': False,
            'removeOutliers': False,
            'resampledPixelSpacing': None,
            'interpolator': 'sitkBSpline',
            'enableCExtensions': True,
            'correctMask': True,
            'label': 255,
            'verbose': False
        }

        extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
        extractor.disableAllFeatures()
        
        extractor.enableImageTypeByName('Original')
        extractor.enableImageTypeByName('LoG', customArgs={'sigma': [1.0, 2.0, 3.0]})
        extractor.enableImageTypeByName('Square')
        extractor.enableImageTypeByName('SquareRoot')
        extractor.enableImageTypeByName('Logarithm')
        extractor.enableImageTypeByName('Exponential')
        extractor.enableImageTypeByName('Gradient')
        extractor.enableImageTypeByName('LBP2D')
        extractor.enableImageTypeByName('LBP3D')

        extractor.enableFeatureClassByName('firstorder')
        extractor.enableFeatureClassByName('glcm')
        extractor.enableFeatureClassByName('glrlm')
        extractor.enableFeatureClassByName('glszm')
        extractor.enableFeatureClassByName('gldm')
        extractor.enableFeatureClassByName('ngtdm')
        extractor.enableFeatureClassByName('shape')

        result = extractor.execute(image, mask)

        return {k.lower(): v.item() if type(v) == np.ndarray else v for k, v in result.items() if 'diagnostics' not in k}

    def extract_radiomic_and_wavelet_features(self, image_path:str, mask_path:str) -> Dict[str, float]:
        radiomic_features = self.extract_features(image_path, mask_path)

        wavelet_types = [
            'haar',
            'dmey',
            *[f'sym{i}' for i in range(2, 21)],
            *[f'db{i}' for i in range(1, 21)],
            *[f'coif{i}' for i in range(1, 6)],
            *[f'bior{v}' for v in ['1.1', '1.3', '1.5', '2.2', '2.4', '2.6', '2.8', '3.1', '3.3', '3.5', '3.7', '3.9', '4.4', '5.5', '6.8']],
            *[f'rbio{v}' for v in ['1.1', '1.3', '1.5', '2.2', '2.4', '2.6', '2.8', '3.1', '3.3', '3.5', '3.7', '3.9', '4.4', '5.5', '6.8']]
        ]

        extractor = featureextractor.RadiomicsFeatureExtractor(**settings)

        for wavelet in wavelet_types:        
            extractor.disableAllFeatures()
            extractor.enableImageTypeByName('Wavelet', customArgs={'wavelet': wavelet})
            extractor.enableFeatureClassByName('firstorder')
            extractor.enableFeatureClassByName('glcm')
            extractor.enableFeatureClassByName('glrlm')
            extractor.enableFeatureClassByName('glszm')
            extractor.enableFeatureClassByName('gldm')
            extractor.enableFeatureClassByName('ngtdm')
            extractor.enableFeatureClassByName('shape')
            
            result = extractor.execute(image, mask)
            radiomics_features =  radiomics_features | {k.lower().replace('wavelet-', f'wavelet-{wavelet}-'): v.item() if type(v) == np.ndarray else v 
                                                        for k, v in result.items() if 'wavelet-' in k}

        return radiomics_features