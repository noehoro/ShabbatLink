'use client';

import React from 'react';
import styles from './Footer.module.css';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.brand}>
          <span className={styles.logo}>✡ ShabbatLink</span>
          <p className={styles.tagline}>
            Conectando comunidad a través de cenas de Shabat
          </p>
          <p className={styles.taglineEn}>
            Connecting community through Shabbat dinners
          </p>
        </div>
        
        <div className={styles.info}>
          <p>Un proyecto del Jewish Latin Center</p>
          <p className={styles.copyright}>
            © {new Date().getFullYear()} JLC. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
