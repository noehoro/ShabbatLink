'use client';

import React from 'react';
import styles from './Checkbox.module.css';

interface CheckboxProps {
  label: React.ReactNode;
  checked: boolean;
  onChange: (checked: boolean) => void;
  error?: string;
  id?: string;
}

export default function Checkbox({
  label,
  checked,
  onChange,
  error,
  id,
}: CheckboxProps) {
  const inputId = id || 'checkbox-' + Math.random().toString(36).substr(2, 9);

  return (
    <div className={styles.container}>
      <label className={styles.label} htmlFor={inputId}>
        <input
          type="checkbox"
          id={inputId}
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          className={styles.checkbox}
        />
        <span className={styles.checkmark}>
          {checked && (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          )}
        </span>
        <span className={styles.text}>{label}</span>
      </label>
      {error && <span className={styles.error}>{error}</span>}
    </div>
  );
}
