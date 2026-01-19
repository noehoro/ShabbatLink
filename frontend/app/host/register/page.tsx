'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Layout } from '../../../components/layout';
import { Button, Card, Alert } from '../../../components/ui';
import { TextInput, Select, MultiSelect, RadioGroup, VibeSlider, Checkbox, Textarea } from '../../../components/form';
import { createHost, ApiError } from '../../../lib/api';
import { NEIGHBORHOODS, LANGUAGES, HOST_KOSHER_OPTIONS, HOST_CONTRIBUTION_OPTIONS, VIBE_LABELS } from '../../../lib/constants';
import styles from './page.module.css';

const SEAT_OPTIONS = Array.from({ length: 20 }, (_, i) => ({
  value: i + 1,
  label: `${i + 1} ${i === 0 ? 'seat' : 'seats'}`,
}));

export default function HostRegister() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    neighborhood: '',
    address: '',
    seats_available: 4,
    languages: ['English'] as string[],
    kosher_level: '',
    contribution_preference: '',
    vibe_chabad: 3,
    vibe_social: 3,
    vibe_formality: 3,
    tagline: '',
    private_notes: '',
    no_show_acknowledged: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.full_name.trim()) newErrors.full_name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Invalid email format';
    if (!formData.phone.trim()) newErrors.phone = 'Phone is required';
    if (!formData.neighborhood) newErrors.neighborhood = 'Neighborhood is required';
    if (!formData.address.trim()) newErrors.address = 'Address is required';
    if (formData.languages.length === 0) newErrors.languages = 'Select at least one language';
    if (!formData.kosher_level) newErrors.kosher_level = 'Kosher level is required';
    if (!formData.contribution_preference) newErrors.contribution_preference = 'Contribution preference is required';
    if (!formData.no_show_acknowledged) newErrors.no_show_acknowledged = 'You must acknowledge the no-show policy';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validate()) return;

    setIsLoading(true);

    try {
      await createHost(formData);
      setSuccess(true);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <Layout maxWidth="md">
        <Card className={styles.successCard}>
          <div className={styles.successIcon}>✓</div>
          <h1>Thank You for Hosting!</h1>
          <p>
            We've sent a confirmation email to <strong>{formData.email}</strong>.
          </p>
          <p>
            You'll receive match requests with guest details soon. You can accept 
            or decline each request, and guest contact info will only be shared 
            after you accept.
          </p>
          <Button onClick={() => router.push('/')}>Return Home</Button>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout maxWidth="md">
      <div className={styles.header}>
        <h1>Host a Shabbat Dinner</h1>
        <p>Open your home and share the joy of Shabbat with our community.</p>
      </div>

      {error && (
        <Alert type="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <form onSubmit={handleSubmit}>
          {/* Personal Info */}
          <section className={styles.section}>
            <h2>Your Information</h2>
            
            <TextInput
              label="Full Name"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              error={errors.full_name}
              required
            />

            <TextInput
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              error={errors.email}
              required
            />

            <TextInput
              label="Phone"
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              error={errors.phone}
              helpText="Will only be shared with confirmed guests"
              required
            />
          </section>

          {/* Location */}
          <section className={styles.section}>
            <h2>Location</h2>

            <Select
              label="Neighborhood"
              options={NEIGHBORHOODS.map(n => n)}
              value={formData.neighborhood}
              onChange={(e) => setFormData({ ...formData, neighborhood: e.target.value })}
              error={errors.neighborhood}
              required
            />

            <Textarea
              label="Full Address"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              error={errors.address}
              placeholder="Street address, apartment number, etc."
              helpText="Only shared with confirmed guests"
              rows={2}
              required
            />

            <Select
              label="Available Seats"
              options={SEAT_OPTIONS}
              value={formData.seats_available}
              onChange={(e) => setFormData({ ...formData, seats_available: parseInt(e.target.value) })}
              helpText="How many guests can you accommodate?"
              required
            />
          </section>

          {/* Preferences */}
          <section className={styles.section}>
            <h2>Your Home</h2>

            <MultiSelect
              label="Languages"
              options={[...LANGUAGES]}
              value={formData.languages}
              onChange={(languages) => setFormData({ ...formData, languages })}
              error={errors.languages}
              helpText="Languages spoken at your dinner"
              required
            />

            <RadioGroup
              label="Kosher Level"
              name="kosher"
              options={[...HOST_KOSHER_OPTIONS]}
              value={formData.kosher_level}
              onChange={(v) => setFormData({ ...formData, kosher_level: v })}
              error={errors.kosher_level}
              required
            />

            <RadioGroup
              label="Contribution Preference"
              name="contribution"
              options={[...HOST_CONTRIBUTION_OPTIONS]}
              value={formData.contribution_preference}
              onChange={(v) => setFormData({ ...formData, contribution_preference: v })}
              error={errors.contribution_preference}
              helpText="Would you like guests to contribute to the meal?"
              required
            />
          </section>

          {/* Vibe */}
          <section className={styles.section}>
            <h2>Your Shabbat Vibe</h2>
            <p className={styles.vibeIntro}>Help us match you with compatible guests.</p>

            <VibeSlider
              label={VIBE_LABELS.chabad.label}
              lowLabel={VIBE_LABELS.chabad.low}
              highLabel={VIBE_LABELS.chabad.high}
              value={formData.vibe_chabad}
              onChange={(v) => setFormData({ ...formData, vibe_chabad: v })}
            />

            <VibeSlider
              label={VIBE_LABELS.social.label}
              lowLabel={VIBE_LABELS.social.low}
              highLabel={VIBE_LABELS.social.high}
              value={formData.vibe_social}
              onChange={(v) => setFormData({ ...formData, vibe_social: v })}
            />

            <VibeSlider
              label={VIBE_LABELS.formality.label}
              lowLabel={VIBE_LABELS.formality.low}
              highLabel={VIBE_LABELS.formality.high}
              value={formData.vibe_formality}
              onChange={(v) => setFormData({ ...formData, vibe_formality: v })}
            />
          </section>

          {/* Optional */}
          <section className={styles.section}>
            <h2>Additional Details</h2>

            <TextInput
              label="What to Expect (Optional)"
              value={formData.tagline}
              onChange={(e) => setFormData({ ...formData, tagline: e.target.value })}
              placeholder="e.g., 'Lively discussion, great food, family-friendly'"
              helpText="A short tagline guests will see"
            />

            <Textarea
              label="Private Notes for Admin (Optional)"
              value={formData.private_notes}
              onChange={(e) => setFormData({ ...formData, private_notes: e.target.value })}
              placeholder="Anything our team should know?"
              helpText="This won't be shared with guests"
            />
          </section>

          {/* Policy */}
          <section className={styles.section}>
            <h2>No-Show Policy</h2>
            <div className={styles.policyBox}>
              <p>
                As a host, you're making a commitment to welcome guests into your home. 
                If your plans change, please notify us as soon as possible so we can 
                find alternative arrangements for your matched guests.
              </p>
              <p>
                You can also report guest no-shows after the event, helping us maintain 
                a reliable community.
              </p>
            </div>

            <Checkbox
              label={
                <span>
                  I understand the hosting commitment and will notify ShabbatLink if 
                  I can no longer host.
                </span>
              }
              checked={formData.no_show_acknowledged}
              onChange={(checked) => setFormData({ ...formData, no_show_acknowledged: checked })}
              error={errors.no_show_acknowledged}
            />
          </section>

          <div className={styles.submitSection}>
            <Button type="submit" size="lg" fullWidth isLoading={isLoading}>
              Register as Host
            </Button>
          </div>
        </form>
      </Card>
    </Layout>
  );
}
