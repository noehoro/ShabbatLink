'use client';

import React from 'react';
import Link from 'next/link';
import styles from './Header.module.css';

interface HeaderProps {
  showNav?: boolean;
}

export default function Header({ showNav = true }: HeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          <span className={styles.logoIcon}>✡</span>
          <span className={styles.logoText}>ShabbatLink</span>
        </Link>
        
        {showNav && (
          <nav className={styles.nav}>
            <Link href="/guest/register" className={styles.navLink}>
              Attend a Dinner
            </Link>
            <Link href="/host/register" className={styles.navLink}>
              Host a Dinner
            </Link>
            <Link href="/auth/login" className={styles.navLinkSecondary}>
              Returning User?
            </Link>
          </nav>
        )}
      </div>
    </header>
  );
}
