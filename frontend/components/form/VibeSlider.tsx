'use client';

import React from 'react';
import styles from './FormField.module.css';
import sliderStyles from './VibeSlider.module.css';

interface VibeSliderProps {
  label: string;
  lowLabel: string;
  highLabel: string;
  value: number;
  onChange: (value: number) => void;
  error?: string;
  helpText?: string;
}

export default function VibeSlider({
  label,
  lowLabel,
  highLabel,
  value,
  onChange,
  error,
  helpText,
}: VibeSliderProps) {
  return (
    <div className={styles.field}>
      <span className={styles.label}>{label}</span>
      <div className={sliderStyles.sliderContainer}>
        <span className={sliderStyles.labelLow}>{lowLabel}</span>
        <div className={sliderStyles.sliderWrapper}>
          <input
            type="range"
            min="1"
            max="5"
            value={value}
            onChange={(e) => onChange(parseInt(e.target.value, 10))}
            className={sliderStyles.slider}
          />
          <div className={sliderStyles.markers}>
            {[1, 2, 3, 4, 5].map((n) => (
              <span
                key={n}
                className={`${sliderStyles.marker} ${value === n ? sliderStyles.active : ''}`}
              >
                {n}
              </span>
            ))}
          </div>
        </div>
        <span className={sliderStyles.labelHigh}>{highLabel}</span>
      </div>
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
