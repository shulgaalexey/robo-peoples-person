"""Core data models for workplace relationship management."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkRelationshipType(str, Enum):
    """Types of workplace relationships."""
    MANAGER = "manager"
    DIRECT_REPORT = "direct_report"
    COLLEAGUE = "colleague"
    CLIENT = "client"
    VENDOR = "vendor"
    COLLABORATOR = "collaborator"
    MENTOR = "mentor"
    MENTEE = "mentee"


class CommunicationPreference(str, Enum):
    """Communication preferences for workplace interactions."""
    EMAIL = "email"
    VIDEO_CALL = "video_call"
    PHONE_CALL = "phone_call"
    CHAT = "chat"
    IN_PERSON = "in_person"
    ASYNC_MESSAGE = "async_message"


class InteractionType(str, Enum):
    """Types of workplace interactions."""
    MEETING = "meeting"
    EMAIL = "email"
    CHAT = "chat"
    PHONE_CALL = "phone_call"
    VIDEO_CALL = "video_call"
    PRESENTATION = "presentation"
    REVIEW = "review"
    BRAINSTORMING = "brainstorming"
    ONE_ON_ONE = "one_on_one"
    TEAM_MEETING = "team_meeting"


class Person(BaseModel):
    """Coworker entity in the workplace social graph."""

    name: str = Field(..., description="Full name of the person")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

    # Work-specific information
    role: Optional[str] = Field(None, description="Job title or role")
    department: Optional[str] = Field(None, description="Department or team")
    manager: Optional[str] = Field(None, description="Manager's name")

    # Expertise and skills
    expertise_areas: List[str] = Field(
        default_factory=list,
        description="Areas of expertise and skills"
    )

    # Communication preferences
    communication_preference: Optional[CommunicationPreference] = Field(
        None, description="Preferred communication method"
    )
    availability: Optional[str] = Field(
        None, description="General availability information"
    )
    timezone: Optional[str] = Field(None, description="Timezone")

    # Interaction tracking
    last_interaction: Optional[datetime] = Field(
        None, description="Last time you interacted with this person"
    )
    interaction_frequency: Optional[str] = Field(
        None, description="How often you typically interact"
    )

    # Additional context
    notes: Optional[str] = Field(
        None, description="Personal notes about this person"
    )
    attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional flexible attributes"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def update_last_interaction(self) -> None:
        """Update the last interaction timestamp."""
        self.last_interaction = datetime.now()
        self.updated_at = datetime.now()


class WorkRelationship(BaseModel):
    """Professional relationship between two people."""

    from_person: str = Field(..., description="Name of the first person")
    to_person: str = Field(..., description="Name of the second person")
    relationship_type: WorkRelationshipType = Field(
        ..., description="Type of relationship"
    )

    # Relationship properties
    bidirectional: bool = Field(
        default=True, description="Whether the relationship is bidirectional"
    )
    strength: Optional[float] = Field(
        None, description="Relationship strength (0.0 to 1.0)", ge=0.0, le=1.0
    )
    context: Optional[str] = Field(
        None, description="Context of the relationship (project, team, etc.)"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = Field(
        None, description="Additional notes about the relationship"
    )

    def is_hierarchical(self) -> bool:
        """Check if the relationship is hierarchical (manager/direct_report)."""
        return self.relationship_type in [
            WorkRelationshipType.MANAGER,
            WorkRelationshipType.DIRECT_REPORT
        ]


class Interaction(BaseModel):
    """Record of a specific interaction with a coworker."""

    with_person: str = Field(..., description="Name of the person interacted with")
    interaction_type: InteractionType = Field(
        ..., description="Type of interaction"
    )

    # Interaction details
    topic: Optional[str] = Field(None, description="What was discussed")
    outcome: Optional[str] = Field(
        None, description="Result or next steps from the interaction"
    )
    duration_minutes: Optional[int] = Field(
        None, description="Duration of the interaction in minutes"
    )

    # Context
    project: Optional[str] = Field(
        None, description="Related project or initiative"
    )
    location: Optional[str] = Field(
        None, description="Location of the interaction"
    )
    participants: List[str] = Field(
        default_factory=list,
        description="Other participants in the interaction"
    )

    # Metadata
    date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = Field(
        None, description="Additional notes about the interaction"
    )
    follow_up_required: bool = Field(
        default=False, description="Whether follow-up is required"
    )
    follow_up_date: Optional[datetime] = Field(
        None, description="When to follow up"
    )

    def mark_follow_up_complete(self) -> None:
        """Mark follow-up as completed."""
        self.follow_up_required = False
        self.follow_up_date = None


class ExpertiseQuery(BaseModel):
    """Query model for finding experts."""

    expertise_area: str = Field(..., description="Area of expertise to search for")
    department: Optional[str] = Field(
        None, description="Filter by department"
    )
    minimum_experience: Optional[str] = Field(
        None, description="Minimum experience level"
    )
    availability_required: bool = Field(
        default=False, description="Whether person must be available"
    )


class NetworkMetrics(BaseModel):
    """Network analysis metrics for a person or group."""

    person_name: Optional[str] = Field(None, description="Person name if individual metrics")

    # Centrality measures
    degree_centrality: Optional[float] = Field(
        None, description="Degree centrality score"
    )
    betweenness_centrality: Optional[float] = Field(
        None, description="Betweenness centrality score"
    )
    closeness_centrality: Optional[float] = Field(
        None, description="Closeness centrality score"
    )
    eigenvector_centrality: Optional[float] = Field(
        None, description="Eigenvector centrality score"
    )

    # Connection counts
    total_connections: Optional[int] = Field(
        None, description="Total number of connections"
    )
    direct_reports: Optional[int] = Field(
        None, description="Number of direct reports"
    )

    # Expertise metrics
    expertise_diversity: Optional[float] = Field(
        None, description="Diversity of expertise areas"
    )
    collaboration_score: Optional[float] = Field(
        None, description="Overall collaboration score"
    )

    # Metadata
    calculated_at: datetime = Field(default_factory=datetime.now)
    graph_size: Optional[int] = Field(
        None, description="Size of the graph when calculated"
    )
