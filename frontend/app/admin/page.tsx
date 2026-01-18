'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button, Card, Alert, Spinner } from '@/components/ui';
import { TextInput } from '@/components/form';
import { adminLogin, setAdminToken, getAdminToken, ApiError } from '@/lib/api';
import styles from './page.module.css';

export default function AdminLoginPage() {
  const router = useRouter();
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isChecking, setIsChecking] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if already logged in
    const token = getAdminToken();
    if (token) {
      router.push('/admin/dashboard');
    } else {
      setIsChecking(false);
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!password) {
      setError('Please enter the admin password');
      return;
    }

    setIsLoading(true);

    try {
      const result = await adminLogin(password);
      setAdminToken(result.token);
      router.push('/admin/dashboard');
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isChecking) {
    return (
      <div className={styles.container}>
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card className={styles.loginCard}>
        <div className={styles.logo}>
          <span>✡</span>
          <span>ShabbatLink</span>
        </div>
        <h1>Admin Panel</h1>
        
        {error && (
          <Alert type="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextInput
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <Button type="submit" fullWidth size="lg" isLoading={isLoading}>
            Log In
          </Button>
        </form>
      </Card>
    </div>
  );
}
