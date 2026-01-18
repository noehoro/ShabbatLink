'use client';

import React from 'react';
import styles from './Spinner.module.css';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  const classNames = [styles.spinner, styles[size], className].filter(Boolean).join(' ');
  return <div className={classNames} />;
}

interface LoadingPageProps {
  message?: string;
}

export function LoadingPage({ message = 'Loading...' }: LoadingPageProps) {
  return (
    <div className={styles.loadingPage}>
      <Spinner size="lg" />
      <p className={styles.loadingMessage}>{message}</p>
    </div>
  );
}
