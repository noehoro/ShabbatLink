'use client';

import React from 'react';
import styles from './FormField.module.css';

interface TextInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helpText?: string;
}

export default function TextInput({
  label,
  error,
  helpText,
  id,
  className = '',
  ...props
}: TextInputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`${styles.field} ${className}`}>
      <label htmlFor={inputId} className={styles.label}>
        {label}
        {props.required && <span className={styles.required}>*</span>}
      </label>
      <input
        id={inputId}
        className={`${styles.input} ${error ? styles.inputError : ''}`}
        {...props}
      />
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
