'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Layout } from '@/components/layout';
import { Button, Card, Alert, Spinner } from '@/components/ui';
import { confirmAttendance, ApiError } from '@/lib/api';
import styles from './page.module.css';

function ConfirmContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [confirmed, setConfirmed] = useState(false);
  const [hostDetails, setHostDetails] = useState<any>(null);

  useEffect(() => {
    if (!token) {
      setError('Invalid link. Please use the link from your reminder email.');
      setIsLoading(false);
      return;
    }

    const confirm = async () => {
      try {
        const result = await confirmAttendance(token);
        setConfirmed(true);
        setHostDetails({
          name: result.host_name,
          address: result.host_address,
          phone: result.host_phone,
        });
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError('Failed to confirm attendance. Please try again.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    confirm();
  }, [token]);

  if (isLoading) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <Spinner size="lg" />
          <p className={styles.loadingText}>Confirming your attendance...</p>
        </Card>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <Alert type="error">{error}</Alert>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout maxWidth="sm" showNav={false}>
      <Card className={styles.card}>
        <div className={styles.icon}>✓</div>
        <h1>You're Confirmed!</h1>
        <p className={styles.subtitle}>
          Thank you for confirming. Have a wonderful Shabbat dinner!
        </p>

        {hostDetails && (
          <div className={styles.details}>
            <h2>Your Dinner Details</h2>
            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Host</span>
              <span className={styles.detailValue}>{hostDetails.name}</span>
            </div>
            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Address</span>
              <span className={styles.detailValue}>{hostDetails.address}</span>
            </div>
            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Phone</span>
              <span className={styles.detailValue}>
                <a href={`tel:${hostDetails.phone}`}>{hostDetails.phone}</a>
              </span>
            </div>
          </div>
        )}

        <p className={styles.reminder}>
          Remember: If your plans change, contact your host immediately.
        </p>
      </Card>
    </Layout>
  );
}

export default function AttendanceConfirmPage() {
  return (
    <Suspense fallback={
      <Layout maxWidth="sm" showNav={false}>
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <Spinner size="lg" />
          <p style={{ marginTop: '1rem', color: 'var(--color-text-light)' }}>
            Loading...
          </p>
        </div>
      </Layout>
    }>
      <ConfirmContent />
    </Suspense>
  );
}
