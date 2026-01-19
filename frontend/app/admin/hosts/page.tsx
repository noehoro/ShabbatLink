'use client';

import React, { useEffect, useState } from 'react';
import { Card, Alert, Spinner, Badge, Button, Modal } from '../../../components/ui';
import { getAdminHosts, getAdminHostDetail, sendHostSummary, sendNoShowReportRequest, ApiError } from '../../../lib/api';
import styles from '../guests/page.module.css';

export default function AdminHostsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hosts, setHosts] = useState<any[]>([]);
  const [selectedHost, setSelectedHost] = useState<any>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [sendingAction, setSendingAction] = useState<string | null>(null);

  useEffect(() => {
    loadHosts();
  }, []);

  const loadHosts = async () => {
    try {
      const data = await getAdminHosts();
      setHosts(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load hosts');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const viewHostDetail = async (id: string) => {
    try {
      const host = await getAdminHostDetail(id);
      setSelectedHost(host);
      setIsModalOpen(true);
    } catch (err) {
      setError('Failed to load host details');
    }
  };

  const handleSendSummary = async (id: string) => {
    setSendingAction(`summary-${id}`);
    try {
      await sendHostSummary(id);
      alert('Host summary sent!');
    } catch (err) {
      setError('Failed to send summary');
    } finally {
      setSendingAction(null);
    }
  };

  const handleSendNoShowRequest = async (id: string) => {
    setSendingAction(`noshow-${id}`);
    try {
      await sendNoShowReportRequest(id);
      alert('No-show report request sent!');
    } catch (err) {
      setError('Failed to send no-show request');
    } finally {
      setSendingAction(null);
    }
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
        <h1>Hosts</h1>
        <span className={styles.count}>{hosts.length} registered</span>
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
              <th>Seats</th>
              <th>Remaining</th>
              <th>Kosher</th>
              <th>Matches</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {hosts.map((host) => (
              <tr key={host.id}>
                <td>
                  <div className={styles.nameCell}>
                    <span className={styles.name}>{host.full_name}</span>
                    <span className={styles.email}>{host.email}</span>
                  </div>
                </td>
                <td>{host.neighborhood}</td>
                <td>{host.seats_available}</td>
                <td>
                  <Badge variant={host.remaining_capacity > 0 ? 'success' : 'default'}>
                    {host.remaining_capacity}
                  </Badge>
                </td>
                <td>{host.kosher_level}</td>
                <td>
                  {host.match_counts?.confirmed > 0 && (
                    <Badge variant="success">{host.match_counts.confirmed} confirmed</Badge>
                  )}
                  {host.match_counts?.accepted > 0 && (
                    <Badge variant="warning">{host.match_counts.accepted} accepted</Badge>
                  )}
                  {host.match_counts?.requested > 0 && (
                    <Badge variant="info">{host.match_counts.requested} pending</Badge>
                  )}
                </td>
                <td>
                  <Button size="sm" variant="ghost" onClick={() => viewHostDetail(host.id)}>
                    View
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {/* Host Detail Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Host Details"
        size="lg"
      >
        {selectedHost && (
          <div className={styles.detail}>
            <div className={styles.detailSection}>
              <h3>Contact Information</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Name</label>
                  <p>{selectedHost.full_name}</p>
                </div>
                <div>
                  <label>Email</label>
                  <p>{selectedHost.email}</p>
                </div>
                <div>
                  <label>Phone</label>
                  <p>{selectedHost.phone}</p>
                </div>
                <div>
                  <label>Address</label>
                  <p>{selectedHost.address}</p>
                </div>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h3>Hosting Details</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Neighborhood</label>
                  <p>{selectedHost.neighborhood}</p>
                </div>
                <div>
                  <label>Total Seats</label>
                  <p>{selectedHost.seats_available}</p>
                </div>
                <div>
                  <label>Remaining</label>
                  <p>{selectedHost.remaining_capacity}</p>
                </div>
                <div>
                  <label>Languages</label>
                  <p>{selectedHost.languages?.join(', ')}</p>
                </div>
                <div>
                  <label>Kosher</label>
                  <p>{selectedHost.kosher_level}</p>
                </div>
                <div>
                  <label>Contribution</label>
                  <p>{selectedHost.contribution_preference}</p>
                </div>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h3>Vibe</h3>
              <div className={styles.detailGrid}>
                <div>
                  <label>Chabad Energy</label>
                  <p>{selectedHost.vibe_chabad}/5</p>
                </div>
                <div>
                  <label>Social Intensity</label>
                  <p>{selectedHost.vibe_social}/5</p>
                </div>
                <div>
                  <label>Formality</label>
                  <p>{selectedHost.vibe_formality}/5</p>
                </div>
              </div>
            </div>

            {selectedHost.tagline && (
              <div className={styles.detailSection}>
                <h3>What to Expect</h3>
                <p className={styles.notes}>{selectedHost.tagline}</p>
              </div>
            )}

            {selectedHost.private_notes && (
              <div className={styles.detailSection}>
                <h3>Private Notes (Admin Only)</h3>
                <p className={styles.notes}>{selectedHost.private_notes}</p>
              </div>
            )}

            <div className={styles.detailSection}>
              <h3>Actions</h3>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                <Button
                  size="sm"
                  variant="ghost"
                  isLoading={sendingAction === `summary-${selectedHost.id}`}
                  onClick={() => handleSendSummary(selectedHost.id)}
                >
                  Send Day-of Summary
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  isLoading={sendingAction === `noshow-${selectedHost.id}`}
                  onClick={() => handleSendNoShowRequest(selectedHost.id)}
                >
                  Send No-Show Report Request
                </Button>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
