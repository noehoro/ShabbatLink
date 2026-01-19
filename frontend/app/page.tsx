'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Layout } from '../components/layout';
import { Button } from '../components/ui';
import styles from './page.module.css';

export default function Home() {
  return (
    <Layout>
      {/* Hero Section with Background Logo */}
      <section className={styles.hero}>
        {/* South America Silhouette Backgrounds */}
        <div className={styles.continentRight}>
          <svg className={styles.continentSvg} viewBox="0 0 200 400" fill="currentColor">
            <path d="M120 10 C145 8, 170 18, 185 38 C195 52, 198 72, 195 95 C192 118, 182 142, 175 168 C168 194, 165 222, 168 250 C171 278, 180 305, 178 332 C176 359, 162 383, 140 398 C118 413, 88 418, 62 410 C36 402, 15 382, 8 355 C1 328, 8 295, 18 265 C28 235, 42 208, 48 178 C54 148, 52 115, 58 85 C64 55, 78 28, 100 15 C107 11, 114 10, 120 10 Z"/>
          </svg>
        </div>
        <div className={styles.continentLeft}>
          <svg className={styles.continentSvgSmall} viewBox="0 0 200 400" fill="currentColor">
            <path d="M120 10 C145 8, 170 18, 185 38 C195 52, 198 72, 195 95 C192 118, 182 142, 175 168 C168 194, 165 222, 168 250 C171 278, 180 305, 178 332 C176 359, 162 383, 140 398 C118 413, 88 418, 62 410 C36 402, 15 382, 8 355 C1 328, 8 295, 18 265 C28 235, 42 208, 48 178 C54 148, 52 115, 58 85 C64 55, 78 28, 100 15 C107 11, 114 10, 120 10 Z"/>
          </svg>
        </div>

        {/* Background Logo Watermark */}
        <div className={styles.heroBackground}>
          <Image 
            src="/jlc-logo.png" 
            alt="" 
            width={800} 
            height={324}
            className={styles.backgroundLogo}
            priority
          />
        </div>
        
        {/* Floating Content Card */}
        <div className={styles.heroContent}>
          <div className={styles.badge}>
            <Image 
              src="/jlc-logo.png" 
              alt="Jewish Latin Center" 
              width={140} 
              height={57}
              className={styles.badgeLogo}
            />
          </div>
          
          <p className={styles.spanishGreeting}>¡Bienvenidos a nuestra mesa!</p>
          
          <h1 className={styles.heroTitle}>
            Find Your Perfect
            <span className={styles.highlight}> Shabbat </span>
            Experience
          </h1>
          
          <p className={styles.heroSubtitle}>
            Connecting guests with welcoming hosts for meaningful 
            Friday night dinners across Manhattan. <em>Como en familia.</em>
          </p>
          
          <div className={styles.heroCtas}>
            <Link href="/guest/register">
              <Button size="lg" className={styles.primaryBtn}>
                <span className={styles.btnIcon}>🍽️</span>
                Quiero Asistir
              </Button>
            </Link>
            <Link href="/host/register">
              <Button size="lg" variant="secondary" className={styles.secondaryBtn}>
                <span className={styles.btnIcon}>🏠</span>
                Quiero Ser Anfitrión
              </Button>
            </Link>
          </div>
          
          <p className={styles.btnSubtext}>
            <span>Join a Dinner</span> · <span>Host a Dinner</span>
          </p>
        </div>

        {/* Decorative Elements */}
        <div className={styles.decorCircle1}></div>
        <div className={styles.decorCircle2}></div>
      </section>

      {/* Stats/Trust Bar */}
      <section className={styles.trustBar}>
        <div className={styles.trustItem}>
          <span className={styles.trustNumber}>100+</span>
          <span className={styles.trustLabel}>Cenas Conectadas</span>
        </div>
        <div className={styles.trustDivider}></div>
        <div className={styles.trustItem}>
          <span className={styles.trustNumber}>50+</span>
          <span className={styles.trustLabel}>Anfitriones</span>
        </div>
        <div className={styles.trustDivider}></div>
        <div className={styles.trustItem}>
          <span className={styles.trustNumber}>Manhattan</span>
          <span className={styles.trustLabel}>Comunidad</span>
        </div>
      </section>

      {/* How It Works - Modern Timeline */}
      <section className={styles.howItWorks}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>Así de Fácil</span>
          <h2 className={styles.sectionTitle}>How It Works</h2>
        </div>
        
        <div className={styles.timeline}>
          <div className={styles.timelineStep}>
            <div className={styles.stepIcon}>
              <span>✍️</span>
            </div>
            <div className={styles.stepContent}>
              <h3>Regístrate</h3>
              <p>Share your preferences and dietary needs in our quick form.</p>
            </div>
          </div>
          
          <div className={styles.timelineConnector}></div>
          
          <div className={styles.timelineStep}>
            <div className={styles.stepIcon}>
              <span>🤝</span>
            </div>
            <div className={styles.stepContent}>
              <h3>Te Conectamos</h3>
              <p>We pair you with compatible hosts based on location & vibe.</p>
            </div>
          </div>
          
          <div className={styles.timelineConnector}></div>
          
          <div className={styles.timelineStep}>
            <div className={styles.stepIcon}>
              <span>🎉</span>
            </div>
            <div className={styles.stepContent}>
              <h3>¡Shabat Shalom!</h3>
              <p>Experience the warmth of a home-cooked Friday dinner.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features - Glass Cards */}
      <section className={styles.features}>
        <div className={styles.featureCard}>
          <div className={styles.featureIconWrap}>
            <span>🔒</span>
          </div>
          <h3>Privacidad Primero</h3>
          <p>Contact details shared only after mutual confirmation.</p>
        </div>
        
        <div className={styles.featureCard}>
          <div className={styles.featureIconWrap}>
            <span>⭐</span>
          </div>
          <h3>Matches con Cariño</h3>
          <p>Every pairing is thoughtfully reviewed by our team.</p>
        </div>
        
        <div className={styles.featureCard}>
          <div className={styles.featureIconWrap}>
            <span>❤️</span>
          </div>
          <h3>Amor de Comunidad</h3>
          <p>Building lasting connections through shared tradition.</p>
        </div>
      </section>

      {/* Final CTA */}
      <section className={styles.finalCta}>
        <div className={styles.ctaContent}>
          <h2>¿Listo para Shabat?</h2>
          <p>Whether you're seeking a warm meal or want to share your table, 
             we're here to make the connection. <em>¡Te esperamos!</em></p>
          <div className={styles.ctaButtons}>
            <Link href="/guest/register">
              <Button size="lg">Encontrar una Cena</Button>
            </Link>
            <Link href="/host/register">
              <Button size="lg" variant="ghost">Abrir Tu Hogar</Button>
            </Link>
          </div>
        </div>
        <div className={styles.ctaLogo}>
          <Image 
            src="/jlc-logo.png" 
            alt="Jewish Latin Center" 
            width={160} 
            height={65}
          />
          <span>Un proyecto del Jewish Latin Center</span>
        </div>
      </section>
    </Layout>
  );
}
