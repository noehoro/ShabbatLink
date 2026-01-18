'use client';

import React from 'react';
import styles from './Badge.module.css';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md';
  className?: string;
}

export default function Badge({
  children,
  variant = 'default',
  size = 'md',
  className = '',
}: BadgeProps) {
  const classNames = [
    styles.badge,
    styles[variant],
    styles[size],
    className,
  ].filter(Boolean).join(' ');

  return <span className={classNames}>{children}</span>;
}
