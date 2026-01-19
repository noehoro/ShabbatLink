'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Layout } from '../../../components/layout';
import { Button, Card, Alert, Spinner, Badge } from '../../../components/ui';
import { respondToMatch, getMatchDetails, ApiError } from '../../../lib/api';
import styles from './page.module.css';

function MatchResponseContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const action = searchParams.get('action');

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matchData, setMatchData] = useState<any>(null);
  const [responseStatus, setResponseStatus] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError('Invalid link. Please use the link from your email.');
      setIsLoading(false);
      return;
    }

    // For direct action links, auto-submit
    if (action === 'accept' || action === 'decline') {
      handleResponse();
    } else {
      // Load match details for preview
      loadMatchDetails();
    }
  }, [token, action]);

  const loadMatchDetails = async () => {
    try {
      // Extract match ID from token (it's encoded in the action token)
      // For now, we'll just show a basic preview
      setIsLoading(false);
    } catch (err) {
      setError('Failed to load match details');
      setIsLoading(false);
    }
  };

  const handleResponse = async () => {
    if (!token) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const result = await respondToMatch(token);
      setResponseStatus(result.status);
      setMatchData(result);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to process your response. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
      setIsLoading(false);
    }
  };

  if (isLoading || isSubmitting) {
    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <Spinner size="lg" />
          <p className={styles.loadingText}>
            {isSubmitting ? 'Processing your response...' : 'Loading...'}
          </p>
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

  // Response submitted - show confirmation
  if (responseStatus) {
    const isAccepted = responseStatus === 'accepted' || responseStatus === 'already_accepted';
    const isDeclined = responseStatus === 'declined' || responseStatus === 'already_declined';

    return (
      <Layout maxWidth="sm" showNav={false}>
        <Card className={styles.card}>
          <div className={`${styles.icon} ${isAccepted ? styles.success : styles.neutral}`}>
            {isAccepted ? '✓' : '✕'}
          </div>
          
          <h1>
            {isAccepted ? 'Guest Accepted!' : 'Request Declined'}
          </h1>
          
          {isAccepted && matchData?.guest_name && (
            <div className={styles.guestInfo}>
              <p><strong>{matchData.guest_name}</strong></p>
              <p>Party of {matchData.party_size}</p>
            </div>
          )}
          
          <p className={styles.message}>
            {isAccepted 
              ? "Thank you! We'll finalize the match and send you the guest's contact information soon."
              : "No problem! We'll find another host for this guest."
            }
          </p>
          
          <Button onClick={() => window.close()} variant="ghost">
            Close Window
          </Button>
        </Card>
      </Layout>
    );
  }

  // Preview mode - show buttons (shouldn't normally happen with direct action links)
  return (
    <Layout maxWidth="sm" showNav={false}>
      <Card className={styles.card}>
        <h1>Respond to Guest Request</h1>
        <p>Use the links in your email to accept or decline this guest request.</p>
      </Card>
    </Layout>
  );
}

export default function MatchRespondPage() {
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
      <MatchResponseContent />
    </Suspense>
  );
}
