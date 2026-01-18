'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, Alert, Spinner, Badge, Button } from '@/components/ui';
import { getDashboard, DashboardStats, ApiError } from '@/lib/api';
import styles from './page.module.css';

export default function AdminDashboard() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<DashboardStats | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const result = await getDashboard();
      setData(result);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load dashboard');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <Alert type="error">{error}</Alert>;
  }

  if (!data) return null;

  const { stats, alerts } = data;

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Dashboard</h1>
        <Link href="/admin/matches">
          <Button>Manage Matches</Button>
        </Link>
      </header>

      {/* Stats Grid */}
      <div className={styles.statsGrid}>
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.total_guests}</div>
          <div className={styles.statLabel}>Total Guests</div>
        </Card>
        
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.total_hosts}</div>
          <div className={styles.statLabel}>Total Hosts</div>
        </Card>
        
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.total_seats}</div>
          <div className={styles.statLabel}>Total Seats</div>
        </Card>
        
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.guests_placed}</div>
          <div className={styles.statLabel}>Guests Placed</div>
        </Card>
        
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.pending_decisions}</div>
          <div className={styles.statLabel}>Pending Decisions</div>
        </Card>
        
        <Card className={styles.statCard}>
          <div className={styles.statValue}>{stats.confirmed_matches}</div>
          <div className={styles.statLabel}>Confirmed</div>
        </Card>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <section className={styles.section}>
          <h2>Alerts</h2>
          <div className={styles.alertsList}>
            {alerts.map((alert, i) => (
              <Alert key={i} type={alert.type}>
                {alert.message}
              </Alert>
            ))}
          </div>
        </section>
      )}

      {/* Quick Actions */}
      <section className={styles.section}>
        <h2>Quick Actions</h2>
        <div className={styles.actions}>
          <Link href="/admin/matches">
            <Card className={styles.actionCard}>
              <span className={styles.actionIcon}>🔗</span>
              <h3>Generate Matches</h3>
              <p>Run the matching algorithm</p>
            </Card>
          </Link>
          
          <Link href="/admin/guests">
            <Card className={styles.actionCard}>
              <span className={styles.actionIcon}>👥</span>
              <h3>View Guests</h3>
              <p>Manage guest registrations</p>
            </Card>
          </Link>
          
          <Link href="/admin/hosts">
            <Card className={styles.actionCard}>
              <span className={styles.actionIcon}>🏠</span>
              <h3>View Hosts</h3>
              <p>Manage host registrations</p>
            </Card>
          </Link>
        </div>
      </section>

      {/* Accepted Awaiting Finalization */}
      {stats.accepted_awaiting > 0 && (
        <section className={styles.section}>
          <Alert type="info">
            <strong>{stats.accepted_awaiting} match(es)</strong> have been accepted by hosts and are awaiting your finalization.{' '}
            <Link href="/admin/matches?status=accepted">Review now →</Link>
          </Alert>
        </section>
      )}
    </div>
  );
}
