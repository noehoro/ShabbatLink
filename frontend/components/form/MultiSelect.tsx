'use client';

import React from 'react';
import styles from './FormField.module.css';
import multiStyles from './MultiSelect.module.css';

interface MultiSelectProps {
  label: string;
  options: string[];
  value: string[];
  onChange: (value: string[]) => void;
  error?: string;
  helpText?: string;
  required?: boolean;
}

export default function MultiSelect({
  label,
  options,
  value,
  onChange,
  error,
  helpText,
  required,
}: MultiSelectProps) {
  const handleToggle = (option: string) => {
    if (value.includes(option)) {
      onChange(value.filter((v) => v !== option));
    } else {
      onChange([...value, option]);
    }
  };

  return (
    <div className={styles.field}>
      <span className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </span>
      <div className={multiStyles.options}>
        {options.map((option) => (
          <button
            key={option}
            type="button"
            className={`${multiStyles.option} ${value.includes(option) ? multiStyles.selected : ''}`}
            onClick={() => handleToggle(option)}
          >
            {option}
          </button>
        ))}
      </div>
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
