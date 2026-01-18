'use client';

import React from 'react';
import styles from './Alert.module.css';

interface AlertProps {
  type: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
  className?: string;
  onClose?: () => void;
}

export default function Alert({
  type,
  title,
  children,
  className = '',
  onClose,
}: AlertProps) {
  const classNames = [styles.alert, styles[type], className].filter(Boolean).join(' ');

  return (
    <div className={classNames} role="alert">
      <div className={styles.icon}>{getIcon(type)}</div>
      <div className={styles.content}>
        {title && <h4 className={styles.title}>{title}</h4>}
        <div className={styles.message}>{children}</div>
      </div>
      {onClose && (
        <button className={styles.close} onClick={onClose} aria-label="Close">
          ×
        </button>
      )}
    </div>
  );
}

function getIcon(type: AlertProps['type']) {
  switch (type) {
    case 'info':
      return 'ℹ️';
    case 'success':
      return '✓';
    case 'warning':
      return '⚠️';
    case 'error':
      return '✕';
  }
}
