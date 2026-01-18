'use client';

import React from 'react';
import styles from './FormField.module.css';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
  helpText?: string;
}

export default function Textarea({
  label,
  error,
  helpText,
  id,
  className = '',
  rows = 4,
  ...props
}: TextareaProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`${styles.field} ${className}`}>
      <label htmlFor={inputId} className={styles.label}>
        {label}
        {props.required && <span className={styles.required}>*</span>}
      </label>
      <textarea
        id={inputId}
        rows={rows}
        className={`${styles.textarea} ${error ? styles.inputError : ''}`}
        {...props}
      />
      {error && <span className={styles.error}>{error}</span>}
      {helpText && !error && <span className={styles.helpText}>{helpText}</span>}
    </div>
  );
}
