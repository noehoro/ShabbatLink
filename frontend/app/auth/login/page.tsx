'use client';

import React, { useState } from 'react';
import { Layout } from '@/components/layout';
import { Button, Card, Alert } from '@/components/ui';
import { TextInput } from '@/components/form';
import { requestMagicLink, ApiError } from '@/lib/api';
import styles from './page.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email.trim()) {
      setError('Please enter your email');
      return;
    }

    setIsLoading(true);

    try {
      await requestMagicLink(email);
      setSuccess(true);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <Layout maxWidth="sm">
        <Card className={styles.card}>
          <div className={styles.icon}>📧</div>
          <h1>Check Your Email</h1>
          <p>
            If an account exists with <strong>{email}</strong>, we've sent 
            a login link. Click the link to access your profile.
          </p>
          <p className={styles.note}>
            The link will expire in 15 minutes. Check your spam folder if 
            you don't see it.
          </p>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout maxWidth="sm">
      <Card className={styles.card}>
        <h1>Welcome Back</h1>
        <p>Enter your email to receive a login link.</p>

        {error && (
          <Alert type="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextInput
            label="Email Address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />

          <Button type="submit" fullWidth size="lg" isLoading={isLoading}>
            Send Login Link
          </Button>
        </form>
      </Card>
    </Layout>
  );
}
