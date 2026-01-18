'use client';

import React from 'react';
import Header from './Header';
import Footer from './Footer';
import styles from './Layout.module.css';

interface LayoutProps {
  children: React.ReactNode;
  showNav?: boolean;
  showFooter?: boolean;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

export default function Layout({
  children,
  showNav = true,
  showFooter = true,
  maxWidth = 'lg',
}: LayoutProps) {
  return (
    <div className={styles.layout}>
      <Header showNav={showNav} />
      <main className={`${styles.main} ${styles[maxWidth]}`}>
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  );
}
