'use client';

import React from 'react';
import styles from './FormField.module.css';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  options: Array<{ value: string | number; label: string } | string>;
  error?: string;
  helpText?: string;
  placeholder?: string;
}

export default function Select({
  label,
  options,
  error,
  helpText,
  placeholder = 'Select an option',
  id,
  className = '',
  ...props
}: SelectProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`${styles.field} ${className}`}>
      <label htmlFor={inputId} className={styles.label}>
        {label}
        {props.required && <span className={styles.required}>*</span>}
      </label>
      <select
        id={inputId}
        className={`${styles.select} ${error ? styles.inputError : ''}`}
        {...props}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => {
          const value = typeof option === 'string' ? option : option.value;
          const label = typeof option === 'string' ? option : option.label;
          return (
            <option key={value} value={value}>
              {label}
            </option>
          );
        })}
      </select>
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
