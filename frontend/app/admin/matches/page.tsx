'use client';

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { Card, Alert, Spinner, Badge, Button, Modal } from '../../../components/ui';
import { Select } from '../../../components/form';
import { 
  getAdminMatches, 
  generateMatches, 
  sendMatchRequest, 
  finalizeMatch, 
  deleteMatch,
  editMatch,
  getAdminHosts,
  sendDayOfReminder,
  ApiError 
} from '../../../lib/api';
import { MATCH_STATUSES } from '../../../lib/constants';
import styles from './page.module.css';

function MatchesContent() {
  const searchParams = useSearchParams();
  const initialStatus = searchParams.get('status') || '';
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [matches, setMatches] = useState<any[]>([]);
  const [hosts, setHosts] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState(initialStatus);
  const [isGenerating, setIsGenerating] = useState(false);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  
  // Edit modal
  const [editingMatch, setEditingMatch] = useState<any>(null);
  const [newHostId, setNewHostId] = useState('');

  useEffect(() => {
    loadData();
  }, [statusFilter]);

  const loadData = async () => {
    try {
      const [matchesData, hostsData] = await Promise.all([
        getAdminMatches(statusFilter || undefined),
        getAdminHosts()
      ]);
      setMatches(matchesData);
      setHosts(hostsData);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load data');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    setSuccess(null);
    
    try {
      const result = await generateMatches();
      setSuccess(`Generated ${result.matches_created} matches. ${result.unmatched_guests.length} guests unmatched.`);
      await loadData();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to generate matches');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSendRequest = async (matchId: string) => {
    setActionLoading(`send-${matchId}`);
    try {
      await sendMatchRequest(matchId);
      setSuccess('Match request sent to host!');
      await loadData();
    } catch (err) {
      setError('Failed to send request');
    } finally {
      setActionLoading(null);
    }
  };

  const handleFinalize = async (matchId: string) => {
    setActionLoading(`finalize-${matchId}`);
    try {
      await finalizeMatch(matchId);
      setSuccess('Match finalized! Both parties have been notified.');
      await loadData();
    } catch (err) {
      setError('Failed to finalize match');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDelete = async (matchId: string) => {
    if (!confirm('Are you sure you want to remove this match?')) return;
    
    setActionLoading(`delete-${matchId}`);
    try {
      await deleteMatch(matchId);
      setSuccess('Match removed');
      await loadData();
    } catch (err) {
      setError('Failed to delete match');
    } finally {
      setActionLoading(null);
    }
  };

  const handleSendReminder = async (matchId: string) => {
    setActionLoading(`reminder-${matchId}`);
    try {
      await sendDayOfReminder(matchId);
      setSuccess('Day-of reminder sent to guest!');
    } catch (err) {
      setError('Failed to send reminder');
    } finally {
      setActionLoading(null);
    }
  };

  const openEditModal = (match: any) => {
    setEditingMatch(match);
    setNewHostId(match.host_id);
  };

  const handleEditSubmit = async () => {
    if (!editingMatch || !newHostId) return;
    
    setActionLoading(`edit-${editingMatch.id}`);
    try {
      await editMatch(editingMatch.id, newHostId);
      setSuccess('Match updated!');
      setEditingMatch(null);
      await loadData();
    } catch (err) {
      setError('Failed to update match');
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusBadge = (status: string) => {
    const config = MATCH_STATUSES[status as keyof typeof MATCH_STATUSES];
    if (!config) return <Badge>{status}</Badge>;
    
    const variants: Record<string, 'default' | 'info' | 'warning' | 'success' | 'error'> = {
      gray: 'default',
      blue: 'info',
      yellow: 'warning',
      green: 'success',
      red: 'error',
    };
    
    return <Badge variant={variants[config.color]}>{config.label}</Badge>;
  };

  const getActionsForMatch = (match: any) => {
    const actions = [];
    
    if (match.status === 'proposed') {
      actions.push(
        <Button
          key="send"
          size="sm"
          isLoading={actionLoading === `send-${match.id}`}
          onClick={() => handleSendRequest(match.id)}
        >
          Send Request
        </Button>,
        <Button
          key="edit"
          size="sm"
          variant="ghost"
          onClick={() => openEditModal(match)}
        >
          Edit
        </Button>,
        <Button
          key="delete"
          size="sm"
          variant="ghost"
          isLoading={actionLoading === `delete-${match.id}`}
          onClick={() => handleDelete(match.id)}
        >
          Remove
        </Button>
      );
    }
    
    if (match.status === 'accepted') {
      actions.push(
        <Button
          key="finalize"
          size="sm"
          isLoading={actionLoading === `finalize-${match.id}`}
          onClick={() => handleFinalize(match.id)}
        >
          Finalize
        </Button>
      );
    }
    
    if (match.status === 'confirmed') {
      actions.push(
        <Button
          key="reminder"
          size="sm"
          variant="ghost"
          isLoading={actionLoading === `reminder-${match.id}`}
          onClick={() => handleSendReminder(match.id)}
        >
          Send Reminder
        </Button>
      );
    }
    
    return actions;
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
        <h1>Matches</h1>
        <Button isLoading={isGenerating} onClick={handleGenerate}>
          Generate Matches
        </Button>
      </header>

      {error && (
        <Alert type="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert type="success" onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Status Filter */}
      <div className={styles.filters}>
        <Select
          label=""
          placeholder="All statuses"
          options={[
            { value: '', label: 'All statuses' },
            { value: 'proposed', label: 'Proposed' },
            { value: 'requested', label: 'Requested' },
            { value: 'accepted', label: 'Accepted' },
            { value: 'declined', label: 'Declined' },
            { value: 'confirmed', label: 'Confirmed' },
          ]}
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        />
        <span className={styles.count}>{matches.length} matches</span>
      </div>

      {/* Matches List */}
      {matches.length === 0 ? (
        <Card className={styles.empty}>
          <p>No matches found. Click "Generate Matches" to run the algorithm.</p>
        </Card>
      ) : (
        <div className={styles.matchesList}>
          {matches.map((match) => (
            <Card key={match.id} className={styles.matchCard}>
              <div className={styles.matchHeader}>
                <div className={styles.matchStatus}>
                  {getStatusBadge(match.status)}
                  {match.match_score && (
                    <span className={styles.score}>Score: {(match.match_score * 100).toFixed(0)}%</span>
                  )}
                </div>
              </div>
              
              <div className={styles.matchContent}>
                <div className={styles.party}>
                  <h4>Guest</h4>
                  <p className={styles.name}>{match.guest?.full_name}</p>
                  <p className={styles.details}>
                    {match.guest?.neighborhood} · Party of {match.guest?.party_size}
                  </p>
                  <p className={styles.details}>
                    {match.guest?.kosher_requirement}
                  </p>
                </div>
                
                <div className={styles.arrow}>→</div>
                
                <div className={styles.party}>
                  <h4>Host</h4>
                  <p className={styles.name}>{match.host?.full_name}</p>
                  <p className={styles.details}>
                    {match.host?.neighborhood} · {match.host?.kosher_level}
                  </p>
                </div>
              </div>
              
              {match.why_its_a_fit && (
                <div className={styles.whyFit}>
                  <strong>Why it's a fit:</strong> {match.why_its_a_fit}
                </div>
              )}
              
              <div className={styles.matchActions}>
                {getActionsForMatch(match)}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Edit Modal */}
      <Modal
        isOpen={!!editingMatch}
        onClose={() => setEditingMatch(null)}
        title="Reassign Host"
      >
        {editingMatch && (
          <div className={styles.editModal}>
            <p>
              Reassigning <strong>{editingMatch.guest?.full_name}</strong> (party of {editingMatch.guest?.party_size})
            </p>
            
            <Select
              label="New Host"
              options={hosts
                .filter(h => h.remaining_capacity >= (editingMatch.guest?.party_size || 1) || h.id === editingMatch.host_id)
                .map(h => ({
                  value: h.id,
                  label: `${h.full_name} (${h.neighborhood}) - ${h.remaining_capacity} seats left`
                }))}
              value={newHostId}
              onChange={(e) => setNewHostId(e.target.value)}
            />
            
            <div className={styles.editActions}>
              <Button variant="ghost" onClick={() => setEditingMatch(null)}>
                Cancel
              </Button>
              <Button 
                isLoading={actionLoading === `edit-${editingMatch.id}`}
                onClick={handleEditSubmit}
              >
                Save Changes
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default function AdminMatchesPage() {
  return (
    <Suspense fallback={
      <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem' }}>
        <Spinner size="lg" />
      </div>
    }>
      <MatchesContent />
    </Suspense>
  );
}
