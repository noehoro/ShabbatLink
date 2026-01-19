'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Layout } from '@/components/layout';
import { Card, Alert, Spinner } from '@/components/ui';
import { verifyMagicLink, setAuthToken, ApiError } from '@/lib/api';
import styles from './page.module.css';

function VerifyContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError('Invalid link. Please request a new login link.');
      setIsLoading(false);
      return;
    }

    const verify = async () => {
      try {
        const result = await verifyMagicLink(token);
        setAuthToken(result.token);
        
        // Redirect to profile edit page based on user type
        if (result.user_type === 'guest') {
          router.push(`/guest/profile?id=${result.user.id}`);
        } else {
          router.push(`/host/profile?id=${result.user.id}`);
        }
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError('Failed to verify link. Please try again.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    verify();
  }, [token, router]);

  if (isLoading) {
    return (
      <Layout maxWidth="sm">
        <Card className={styles.loadingCard}>
          <Spinner size="lg" />
          <p className={styles.loadingText}>
            Verifying your link...
          </p>
        </Card>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout maxWidth="sm">
        <Card className={styles.card}>
          <Alert type="error">{error}</Alert>
          <p className={styles.link}>
            <a href="/auth/login">Request a new login link</a>
          </p>
        </Card>
      </Layout>
    );
  }

  return null;
}

export default function VerifyPage() {
  return (
    <Suspense fallback={
      <Layout maxWidth="sm">
        <div className={styles.loadingCard}>
          <Spinner size="lg" />
          <p className={styles.loadingText}>
            Loading...
          </p>
        </div>
      </Layout>
    }>
      <VerifyContent />
    </Suspense>
  );
}
