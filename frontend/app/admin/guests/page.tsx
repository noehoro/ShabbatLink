'use client';

import React, { useEffect, useState } from 'react';
import { Card, Alert, Spinner, Badge, Button, Modal } from '../../../components/ui';
import { getAdminGuests, getAdminGuestDetail, flagGuest, ApiError } from '../../../lib/api';
import { MATCH_STATUSES } from '../../../lib/constants';
import styles from './page.module.css';

export default function AdminGuestsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [guests, setGuests] = useState<any[]>([]);
  const [selectedGuest, setSelectedGuest] = useState<any>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [flaggingId, setFlaggingId] = useState<string | null>(null);

  useEffect(() => {
    loadGuests();
  }, []);

  const loadGuests = async () => {
    try {
      const data = await getAdminGuests();
      setGuests(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load guests');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const viewGuestDetail = async (id: string) => {
    try {
      const guest = await getAdminGuestDetail(id);
      setSelectedGuest(guest);
      setIsModalOpen(true);
    } catch (err) {
      setError('Failed to load guest details');
    }
  };

  const handleFlagGuest = async (id: string) => {
    setFlaggingId(id);
    try {
      await flagGuest(id, 'Flagged by admin', true);
      await loadGuests();
      if (selectedGuest?.id === id) {
        const updated = await getAdminGuestDetail(id);
        setSelectedGuest(updated);
      }
    } catch (err) {
      setError('Failed to flag guest');
    } finally {
      setFlaggingId(null);
    }
  };

  const getStatusBadge = (status: string) => {
    const config = MATCH_STATUSES[status as keyof typeof MATCH_STATUSES];
    if (!config) {
      return <Badge variant="default">Unmatched</Badge>;
    }
    
    const variants: Record<string, 'default' | 'info' | 'warning' | 'success' | 'error'> = {
      gray: 'default',
      blue: 'info',
      yellow: 'warning',
      green: 'success',
      red: 'error',
    };
    
    return <Badge variant={variants[config.color]}>{config.label}</Badge>;
  };

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Guests</h1>
        <span className={styles.count}>{guests.length} registered</span>
      </header>

      {error && (
        <Alert type="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card padding="none">
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Neighborhood</th>
              <th>Party Size</th>
              <th>Kosher</th>
              <th>Status</th>
              <th>Flags</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {guests.map((guest) => (
              <tr key={guest.id}>
                <td>
                  <div className={styles.nameCell}>
                    <span className={styles.name}>{guest.full_name}</span>
                    <span className={styles.email}>{guest.email}</span>
                  </div>
                </td>
                <td>{guest.neighborhood}</td>
                <td>{guest.party_size}</td>
                <td>{guest.kosher_requirement}</td>
                <td>{getStatusBadge(guest.match_status)}</td>
                <td>
                  {guest.is_flagged && <Badge variant="error">Flagged</Badge>}
                  {guest.no_show_count > 0 && (
                    <Badge variant="warning">{guest.no_show_count} no-show{guest.no_show_count > 1 ? 's' : ''}</Badge>
                  )}
                </td>
                <td>
                  <Button size="sm" variant="ghost" onClick={() => viewGuestDetail(guest.id)}>
                    View
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {/* Guest Detail Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Guest Details"
        size="lg"
      >
        {selectedGuest && (
          <div className={styles.detail}>
            <div className={styles.detailSection}>
              <h3>Contact Information</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Name</label>
                  <p>{selectedGuest.full_name}</p>
                </div>
                <div>
                  <label>Email</label>
                  <p>{selectedGuest.email}</p>
                </div>
                <div>
                  <label>Phone</label>
                  <p>{selectedGuest.phone}</p>
                </div>
                <div>
                  <label>Party Size</label>
                  <p>{selectedGuest.party_size}</p>
                </div>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h3>Preferences</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Neighborhood</label>
                  <p>{selectedGuest.neighborhood}</p>
                </div>
                <div>
                  <label>Max Travel</label>
                  <p>{selectedGuest.max_travel_time} min</p>
                </div>
                <div>
                  <label>Languages</label>
                  <p>{selectedGuest.languages?.join(', ')}</p>
                </div>
                <div>
                  <label>Kosher</label>
                  <p>{selectedGuest.kosher_requirement}</p>
                </div>
                <div>
                  <label>Contribution</label>
                  <p>{selectedGuest.contribution_range}</p>
                </div>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h3>Vibe</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Chabad Energy</label>
                  <p>{selectedGuest.vibe_chabad}/5</p>
                </div>
                <div>
                  <label>Social Intensity</label>
                  <p>{selectedGuest.vibe_social}/5</p>
                </div>
                <div>
                  <label>Formality</label>
                  <p>{selectedGuest.vibe_formality}/5</p>
                </div>
              </div>
            </div>

            {selectedGuest.notes_to_admin && (
              <div className={styles.detailSection}>
                <h3>Notes to Admin</h3>
                <p className={styles.notes}>{selectedGuest.notes_to_admin}</p>
              </div>
            )}

            <div className={styles.detailSection}>
              <h3>Status</h3>
              <div className={styles.statusRow}>
                <div>
                  <label>No-Show Count</label>
                  <p>{selectedGuest.no_show_count}</p>
                </div>
                <div>
                  <label>Flagged</label>
                  <p>{selectedGuest.is_flagged ? 'Yes' : 'No'}</p>
                </div>
              </div>
              
              {!selectedGuest.is_flagged && (
                <Button
                  variant="danger"
                  size="sm"
                  isLoading={flaggingId === selectedGuest.id}
                  onClick={() => handleFlagGuest(selectedGuest.id)}
                >
                  Flag Guest
                </Button>
              )}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
