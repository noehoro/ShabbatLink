'use client';

import React from 'react';
import styles from './FormField.module.css';
import radioStyles from './RadioGroup.module.css';

interface RadioGroupProps {
  label: string;
  name: string;
  options: string[];
  value: string;
  onChange: (value: string) => void;
  error?: string;
  helpText?: string;
  required?: boolean;
}

export default function RadioGroup({
  label,
  name,
  options,
  value,
  onChange,
  error,
  helpText,
  required,
}: RadioGroupProps) {
  return (
    <div className={styles.field}>
      <span className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </span>
      <div className={radioStyles.options}>
        {options.map((option) => (
          <label key={option} className={radioStyles.option}>
            <input
              type="radio"
              name={name}
              value={option}
              checked={value === option}
              onChange={(e) => onChange(e.target.value)}
              className={radioStyles.radio}
            />
            <span className={radioStyles.label}>{option}</span>
          </label>
        ))}
      </div>
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
