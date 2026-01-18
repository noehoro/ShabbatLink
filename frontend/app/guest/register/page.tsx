'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Layout } from '@/components/layout';
import { Button, Card, Alert } from '@/components/ui';
import { TextInput, Select, MultiSelect, RadioGroup, VibeSlider, Checkbox, Textarea } from '@/components/form';
import { createGuest, ApiError } from '@/lib/api';
import { NEIGHBORHOODS, TRAVEL_TIMES, LANGUAGES, GENDER_OPTIONS, GUEST_KOSHER_OPTIONS, VIBE_LABELS } from '@/lib/constants';
import styles from './page.module.css';

const PARTY_SIZES = [
  { value: 1, label: '1 person (just me)' },
  { value: 2, label: '2 people' },
];

export default function GuestRegister() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    gender: '',
    party_size: 1,
    neighborhood: '',
    max_travel_time: 30,
    languages: ['English'] as string[],
    kosher_requirement: '',
    contribution_amount: 30,
    vibe_chabad: 3,
    vibe_social: 3,
    vibe_formality: 3,
    attended_jlc_before: false,
    facebook_url: '',
    instagram_handle: '',
    notes_to_admin: '',
    no_show_acknowledged: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.full_name.trim()) newErrors.full_name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Invalid email format';
    if (!formData.phone.trim()) newErrors.phone = 'Phone is required';
    if (!formData.gender) newErrors.gender = 'Gender is required';
    if (!formData.neighborhood) newErrors.neighborhood = 'Neighborhood is required';
    if (formData.languages.length === 0) newErrors.languages = 'Select at least one language';
    if (!formData.kosher_requirement) newErrors.kosher_requirement = 'Kosher preference is required';
    
    // At least one social media field required
    const hasFacebook = formData.facebook_url.trim().length > 0;
    const hasInstagram = formData.instagram_handle.trim().length > 0;
    if (!hasFacebook && !hasInstagram) {
      newErrors.social = 'Please provide at least one: Facebook URL or Instagram handle';
    }
    // Validate Facebook URL format if provided
    if (hasFacebook && !formData.facebook_url.includes('facebook.com') && !formData.facebook_url.includes('fb.com')) {
      newErrors.facebook_url = 'Please enter a valid Facebook URL';
    }
    
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
      // Transform contribution data for API
      const submitData = {
        ...formData,
        contribution_range: `$${formData.contribution_amount}`,
      };
      await createGuest(submitData);
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
          <h1>Registration Complete!</h1>
          <p>
            Thank you for signing up for ShabbatLink! We've sent a confirmation 
            email to <strong>{formData.email}</strong>.
          </p>
          <p>
            Our team will review your preferences and work on finding you the 
            perfect Shabbat dinner match. You'll hear from us soon!
          </p>
          <Button onClick={() => router.push('/')}>Return Home</Button>
        </Card>
      </Layout>
    );
  }

  return (
    <Layout maxWidth="md">
      <div className={styles.header}>
        <h1>Join a Shabbat Dinner</h1>
        <p>Tell us about yourself so we can find you the perfect host.</p>
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
              helpText="Will only be shared with your host after matching"
              required
            />

            <Select
              label="Gender"
              options={GENDER_OPTIONS.map(g => g)}
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
              error={errors.gender}
              required
            />

            <Select
              label="Party Size"
              options={PARTY_SIZES}
              value={formData.party_size}
              onChange={(e) => setFormData({ ...formData, party_size: parseInt(e.target.value) })}
              required
            />
          </section>

          {/* Social Verification */}
          <section className={styles.section}>
            <h2>Social Verification</h2>
            <p className={styles.sectionIntro}>For security purposes, please provide at least one of the following.</p>

            {errors.social && (
              <div className={styles.socialError}>{errors.social}</div>
            )}

            <TextInput
              label="Facebook Profile URL"
              type="url"
              value={formData.facebook_url}
              onChange={(e) => setFormData({ ...formData, facebook_url: e.target.value })}
              error={errors.facebook_url}
              placeholder="https://facebook.com/yourprofile"
              helpText="Your full Facebook profile URL"
            />

            <TextInput
              label="Instagram Handle"
              value={formData.instagram_handle}
              onChange={(e) => setFormData({ ...formData, instagram_handle: e.target.value })}
              error={errors.instagram_handle}
              placeholder="@yourhandle"
              helpText="Your Instagram username (with or without @)"
            />
          </section>

          {/* Location */}
          <section className={styles.section}>
            <h2>Location Preferences</h2>

            <Select
              label="Your Neighborhood"
              options={NEIGHBORHOODS.map(n => n)}
              value={formData.neighborhood}
              onChange={(e) => setFormData({ ...formData, neighborhood: e.target.value })}
              error={errors.neighborhood}
              required
            />

            <Select
              label="Max Travel Time"
              options={TRAVEL_TIMES.map(t => ({ value: t.value, label: t.label }))}
              value={formData.max_travel_time}
              onChange={(e) => setFormData({ ...formData, max_travel_time: parseInt(e.target.value) })}
              helpText="How far are you willing to travel for dinner?"
              required
            />
          </section>

          {/* Preferences */}
          <section className={styles.section}>
            <h2>Your Preferences</h2>

            <MultiSelect
              label="Languages"
              options={[...LANGUAGES]}
              value={formData.languages}
              onChange={(languages) => setFormData({ ...formData, languages })}
              error={errors.languages}
              helpText="Select all that apply"
              required
            />

            {/* Contribution Slider */}
            <div className={styles.contributionSection}>
              <label className={styles.contributionLabel}>
                Contribution to Help Cover Costs
                <span className={styles.contributionSubtext}>
                  Most guests contribute around $25-35 to help hosts with meal expenses
                </span>
              </label>
              
              <div className={styles.contributionSliderWrapper}>
                <div className={styles.contributionAmount}>
                  <span className={styles.contributionDollar}>$</span>
                  <span className={styles.contributionValue}>{formData.contribution_amount}</span>
                </div>
                
                <div className={styles.sliderContainer}>
                  <input
                    type="range"
                    min="10"
                    max="50"
                    step="5"
                    value={formData.contribution_amount}
                    onChange={(e) => setFormData({ ...formData, contribution_amount: parseInt(e.target.value) })}
                    className={styles.contributionSlider}
                  />
                  <div className={styles.sliderMarks}>
                    <span>$10</span>
                    <span className={styles.sliderMarkPopular}>$30</span>
                    <span>$50</span>
                  </div>
                </div>
              </div>

              <p className={styles.contributionHelp}>
                Your contribution helps cover ingredients and preparation. <em>Gracias por tu generosidad.</em>
              </p>
            </div>

            <RadioGroup
              label="Kosher Requirement"
              name="kosher"
              options={[...GUEST_KOSHER_OPTIONS]}
              value={formData.kosher_requirement}
              onChange={(v) => setFormData({ ...formData, kosher_requirement: v })}
              error={errors.kosher_requirement}
              required
            />
          </section>

          {/* Vibe */}
          <section className={styles.section}>
            <h2>Your Shabbat Vibe</h2>
            <p className={styles.vibeIntro}>Help us find a dinner that matches your style.</p>

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

          {/* JLC History */}
          <section className={styles.section}>
            <h2>JLC Experience</h2>

            <Checkbox
              label="I have attended a JLC event before"
              checked={formData.attended_jlc_before}
              onChange={(checked) => setFormData({ ...formData, attended_jlc_before: checked })}
            />
          </section>

          {/* Notes */}
          <section className={styles.section}>
            <h2>Anything Else?</h2>

            <Textarea
              label="Notes to Admin (Optional)"
              value={formData.notes_to_admin}
              onChange={(e) => setFormData({ ...formData, notes_to_admin: e.target.value })}
              placeholder="Any special requests or information we should know?"
            />
          </section>

          {/* Policy */}
          <section className={styles.section}>
            <h2>No-Show Policy</h2>
            <div className={styles.policyBox}>
              <p>
                ShabbatLink operates on trust. Our hosts generously open their homes 
                and prepare meals for guests. <strong>Not showing up without notice is 
                not acceptable.</strong>
              </p>
              <p>
                If your plans change, you must contact your host immediately. 
                Guests who no-show may be blocked from future ShabbatLink events.
              </p>
            </div>

            <Checkbox
              label={
                <span>
                  I understand and agree to the no-show policy. I commit to attending 
                  or notifying my host if I cannot make it.
                </span>
              }
              checked={formData.no_show_acknowledged}
              onChange={(checked) => setFormData({ ...formData, no_show_acknowledged: checked })}
              error={errors.no_show_acknowledged}
            />
          </section>

          <div className={styles.submitSection}>
            <Button type="submit" size="lg" fullWidth isLoading={isLoading}>
              Register for Shabbat Dinner
            </Button>
          </div>
        </form>
      </Card>
    </Layout>
  );
}
