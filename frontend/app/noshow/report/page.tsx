'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Layout } from '../../../components/layout';
import { Button, Card, Alert, Spinner } from '../../../components/ui';
import { Checkbox } from '../../../components/form';
import { getNoShowReportForm, submitNoShowReport, ApiError } from '../../../lib/api';
import styles from './page.module.css';

interface Guest {
  match_id: string;
  guest_name: string;
  party_size: number;
}

function NoShowReportContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [hostName, setHostName] = useState('');
  const [guests, setGuests] = useState<Guest[]>([]);
  const [noShowIds, setNoShowIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!token) {
      setError('Invalid link. Please use the link from your email.');
      setIsLoading(false);
      return;
    }

    const loadForm = async () => {
      try {
        const data = await getNoShowReportForm(token);
        setHostName(data.host_name);
        setGuests(data.guests);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError('Failed to load report form.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadForm();
  }, [token]);

  const toggleNoShow = (matchId: string) => {
    setNoShowIds(prev => {
      const next = new Set(prev);
      if (next.has(matchId)) {
        next.delete(matchId);
      } else {
        next.add(matchId);
      }
      return next;
    });
  };

  const handleSubmit = async () => {
    if (!token) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await submitNoShowReport(token, Array.from(noShowIds));
      setSubmitted(true);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to submit report.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <Spinner size="lg" />
          <p className={styles.loadingText}>Loading...</p>
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

  if (submitted) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <div className={styles.icon}>✓</div>
          <h1>Report Submitted</h1>
          <p>Thank you for letting us know. We'll follow up with any guests who didn't attend.</p>
        </Card>
      </Layout>
    );
  }

  if (guests.length === 0) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <h1>No Guests to Report</h1>
          <p>All your confirmed guests have already been accounted for, or you had no guests confirmed for this dinner.</p>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout maxWidth="sm" showNav={false}>
      <Card className={styles.card}>
        <h1>Report No-Shows</h1>
        <p className={styles.subtitle}>
          Hi {hostName}! Please let us know if any guests didn't show up.
        </p>

        <div className={styles.guestList}>
          {guests.map((guest) => (
            <div key={guest.match_id} className={styles.guestItem}>
              <Checkbox
                label={
                  <span>
                    <strong>{guest.guest_name}</strong>
                    <span className={styles.partySize}> (party of {guest.party_size})</span>
                  </span>
                }
                checked={noShowIds.has(guest.match_id)}
                onChange={() => toggleNoShow(guest.match_id)}
              />
            </div>
          ))}
        </div>

        <p className={styles.hint}>
          Check the box for any guests who did NOT show up.
        </p>

        <div className={styles.actions}>
          <Button 
            onClick={handleSubmit} 
            isLoading={isSubmitting}
            fullWidth
          >
            {noShowIds.size > 0 
              ? `Report ${noShowIds.size} No-Show${noShowIds.size > 1 ? 's' : ''}`
              : 'All Guests Attended'
            }
          </Button>
        </div>
      </Card>
    </Layout>
  );
}

export default function NoShowReportPage() {
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
      <NoShowReportContent />
    </Suspense>
  );
}
