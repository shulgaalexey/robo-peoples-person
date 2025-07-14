"""Tests for data models."""

from datetime import datetime
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from src.database.models import (CommunicationPreference, ExpertiseQuery,
                                 Interaction, InteractionType, NetworkMetrics,
                                 Person, WorkRelationship,
                                 WorkRelationshipType)


def test_person_model():
    """Test Person model validation and serialization."""
    person = Person(
        name="John Doe",
        email="john.doe@company.com",
        role="Senior Developer",
        department="Engineering",
        expertise_areas=["Python", "React", "AWS"]
    )

    assert person.name == "John Doe"
    assert person.email == "john.doe@company.com"
    assert person.role == "Senior Developer"
    assert person.department == "Engineering"
    assert "Python" in person.expertise_areas


def test_person_model_minimal():
    """Test Person model with minimal required fields."""
    person = Person(name="Jane Smith")

    assert person.name == "Jane Smith"
    assert person.email is None
    assert person.role is None
    assert person.department is None
    assert person.expertise_areas == []


def test_person_model_with_all_fields():
    """Test Person model with all fields populated."""
    person = Person(
        name="Alice Johnson",
        email="alice@company.com",
        phone="+1-555-0123",
        role="Product Manager",
        department="Product",
        manager="Bob Wilson",
        expertise_areas=["Product Strategy", "User Research"],
        communication_preference=CommunicationPreference.VIDEO_CALL,
        availability="9-5 EST",
        timezone="US/Eastern",
        notes="Great at cross-team collaboration",
        attributes={"seniority": "senior", "location": "remote"}
    )

    assert person.name == "Alice Johnson"
    assert person.email == "alice@company.com"
    assert person.phone == "+1-555-0123"
    assert person.role == "Product Manager"
    assert person.department == "Product"
    assert person.manager == "Bob Wilson"
    assert person.expertise_areas == ["Product Strategy", "User Research"]
    assert person.communication_preference == CommunicationPreference.VIDEO_CALL
    assert person.availability == "9-5 EST"
    assert person.timezone == "US/Eastern"
    assert person.notes == "Great at cross-team collaboration"
    assert person.attributes["seniority"] == "senior"
    assert person.attributes["location"] == "remote"


def test_person_update_last_interaction():
    """Test updating last interaction timestamp."""
    person = Person(name="Test Person")
    original_updated_at = person.updated_at

    # Wait a tiny bit to ensure timestamp difference
    import time
    time.sleep(0.01)

    person.update_last_interaction()

    assert person.last_interaction is not None
    assert person.updated_at > original_updated_at


def test_work_relationship_type_enum():
    """Test WorkRelationshipType enum values."""
    assert WorkRelationshipType.MANAGER.value == "manager"
    assert WorkRelationshipType.DIRECT_REPORT.value == "direct_report"
    assert WorkRelationshipType.COLLEAGUE.value == "colleague"
    assert WorkRelationshipType.CLIENT.value == "client"
    assert WorkRelationshipType.VENDOR.value == "vendor"
    assert WorkRelationshipType.COLLABORATOR.value == "collaborator"
    assert WorkRelationshipType.MENTOR.value == "mentor"
    assert WorkRelationshipType.MENTEE.value == "mentee"


def test_work_relationship_model():
    """Test WorkRelationship model."""
    relationship = WorkRelationship(
        from_person="John Doe",
        to_person="Jane Smith",
        relationship_type=WorkRelationshipType.COLLEAGUE,
        strength=0.8,
        context="Engineering team collaboration"
    )

    assert relationship.from_person == "John Doe"
    assert relationship.to_person == "Jane Smith"
    assert relationship.relationship_type == WorkRelationshipType.COLLEAGUE
    assert relationship.strength == 0.8
    assert relationship.context == "Engineering team collaboration"
    assert relationship.bidirectional == True  # default


def test_work_relationship_hierarchical():
    """Test hierarchical relationship detection."""
    manager_rel = WorkRelationship(
        from_person="Manager",
        to_person="Employee",
        relationship_type=WorkRelationshipType.MANAGER
    )

    report_rel = WorkRelationship(
        from_person="Employee",
        to_person="Manager",
        relationship_type=WorkRelationshipType.DIRECT_REPORT
    )

    colleague_rel = WorkRelationship(
        from_person="Person A",
        to_person="Person B",
        relationship_type=WorkRelationshipType.COLLEAGUE
    )

    assert manager_rel.is_hierarchical() == True
    assert report_rel.is_hierarchical() == True
    assert colleague_rel.is_hierarchical() == False


def test_work_relationship_validation():
    """Test WorkRelationship validation."""
    # Test strength bounds
    with pytest.raises(ValidationError):
        WorkRelationship(
            from_person="A",
            to_person="B",
            relationship_type=WorkRelationshipType.COLLEAGUE,
            strength=1.5  # > 1.0
        )

    with pytest.raises(ValidationError):
        WorkRelationship(
            from_person="A",
            to_person="B",
            relationship_type=WorkRelationshipType.COLLEAGUE,
            strength=-0.1  # < 0.0
        )


def test_communication_preference_enum():
    """Test CommunicationPreference enum."""
    assert CommunicationPreference.EMAIL.value == "email"
    assert CommunicationPreference.VIDEO_CALL.value == "video_call"
    assert CommunicationPreference.PHONE_CALL.value == "phone_call"
    assert CommunicationPreference.CHAT.value == "chat"
    assert CommunicationPreference.IN_PERSON.value == "in_person"
    assert CommunicationPreference.ASYNC_MESSAGE.value == "async_message"


def test_interaction_type_enum():
    """Test InteractionType enum."""
    assert InteractionType.MEETING.value == "meeting"
    assert InteractionType.EMAIL.value == "email"
    assert InteractionType.CHAT.value == "chat"
    assert InteractionType.PHONE_CALL.value == "phone_call"
    assert InteractionType.VIDEO_CALL.value == "video_call"
    assert InteractionType.PRESENTATION.value == "presentation"
    assert InteractionType.REVIEW.value == "review"
    assert InteractionType.BRAINSTORMING.value == "brainstorming"
    assert InteractionType.ONE_ON_ONE.value == "one_on_one"
    assert InteractionType.TEAM_MEETING.value == "team_meeting"


def test_interaction_model():
    """Test Interaction model."""
    interaction = Interaction(
        with_person="Alice Johnson",
        interaction_type=InteractionType.ONE_ON_ONE,
        topic="Project planning discussion",
        outcome="Agreed on next steps for Q1",
        duration_minutes=30,
        project="Customer Portal v2",
        location="Conference Room A",
        participants=["Bob Wilson"],
        notes="Follow up needed on budget approval",
        follow_up_required=True
    )

    assert interaction.with_person == "Alice Johnson"
    assert interaction.interaction_type == InteractionType.ONE_ON_ONE
    assert interaction.topic == "Project planning discussion"
    assert interaction.outcome == "Agreed on next steps for Q1"
    assert interaction.duration_minutes == 30
    assert interaction.project == "Customer Portal v2"
    assert interaction.location == "Conference Room A"
    assert "Bob Wilson" in interaction.participants
    assert interaction.notes == "Follow up needed on budget approval"
    assert interaction.follow_up_required == True


def test_interaction_mark_follow_up_complete():
    """Test marking interaction follow-up as complete."""
    interaction = Interaction(
        with_person="Test Person",
        interaction_type=InteractionType.EMAIL,
        follow_up_required=True,
        follow_up_date=datetime.now()
    )

    assert interaction.follow_up_required == True
    assert interaction.follow_up_date is not None

    interaction.mark_follow_up_complete()

    assert interaction.follow_up_required == False
    assert interaction.follow_up_date is None


def test_expertise_query_model():
    """Test ExpertiseQuery model."""
    query = ExpertiseQuery(
        expertise_area="Machine Learning",
        department="Data Science",
        minimum_experience="Senior",
        availability_required=True
    )

    assert query.expertise_area == "Machine Learning"
    assert query.department == "Data Science"
    assert query.minimum_experience == "Senior"
    assert query.availability_required == True


def test_expertise_query_minimal():
    """Test ExpertiseQuery with minimal fields."""
    query = ExpertiseQuery(expertise_area="Python")

    assert query.expertise_area == "Python"
    assert query.department is None
    assert query.minimum_experience is None
    assert query.availability_required == False


def test_network_metrics_model():
    """Test NetworkMetrics model."""
    metrics = NetworkMetrics(
        person_name="John Doe",
        degree_centrality=0.75,
        betweenness_centrality=0.45,
        closeness_centrality=0.60,
        eigenvector_centrality=0.80,
        total_connections=15,
        direct_reports=3,
        expertise_diversity=0.85,
        collaboration_score=0.90,
        graph_size=50
    )

    assert metrics.person_name == "John Doe"
    assert metrics.degree_centrality == 0.75
    assert metrics.betweenness_centrality == 0.45
    assert metrics.closeness_centrality == 0.60
    assert metrics.eigenvector_centrality == 0.80
    assert metrics.total_connections == 15
    assert metrics.direct_reports == 3
    assert metrics.expertise_diversity == 0.85
    assert metrics.collaboration_score == 0.90
    assert metrics.graph_size == 50


def test_network_metrics_minimal():
    """Test NetworkMetrics with minimal fields."""
    metrics = NetworkMetrics()

    assert metrics.person_name is None
    assert metrics.degree_centrality is None
    assert metrics.total_connections is None
    assert metrics.calculated_at is not None  # should be set by default


def test_person_model_serialization():
    """Test Person model serialization."""
    person = Person(
        name="Serializable Person",
        email="test@example.com",
        role="Developer",
        department="Engineering",
        expertise_areas=["Python", "Docker"]
    )

    person_dict = person.model_dump()

    assert isinstance(person_dict, dict)
    assert person_dict["name"] == "Serializable Person"
    assert person_dict["email"] == "test@example.com"
    assert person_dict["role"] == "Developer"
    assert person_dict["department"] == "Engineering"
    assert person_dict["expertise_areas"] == ["Python", "Docker"]


def test_work_relationship_serialization():
    """Test WorkRelationship serialization."""
    relationship = WorkRelationship(
        from_person="A",
        to_person="B",
        relationship_type=WorkRelationshipType.MENTOR,
        strength=0.9
    )

    rel_dict = relationship.model_dump()

    assert isinstance(rel_dict, dict)
    assert rel_dict["from_person"] == "A"
    assert rel_dict["to_person"] == "B"
    assert rel_dict["relationship_type"] == "mentor"
    assert rel_dict["strength"] == 0.9


def test_interaction_serialization():
    """Test Interaction serialization."""
    interaction = Interaction(
        with_person="Test Person",
        interaction_type=InteractionType.MEETING,
        topic="Weekly sync"
    )

    interaction_dict = interaction.model_dump()

    assert isinstance(interaction_dict, dict)
    assert interaction_dict["with_person"] == "Test Person"
    assert interaction_dict["interaction_type"] == "meeting"
    assert interaction_dict["topic"] == "Weekly sync"


def test_model_copy():
    """Test model copy functionality."""
    original = Person(name="Original", email="original@test.com")
    copied = original.model_copy(update={"name": "Copied"})

    assert original.name == "Original"
    assert copied.name == "Copied"
    assert copied.email == "original@test.com"  # unchanged


def test_model_defaults():
    """Test model field defaults."""
    person = Person(name="Test")
    assert person.expertise_areas == []
    assert person.attributes == {}
    assert person.created_at is not None
    assert person.updated_at is not None

    relationship = WorkRelationship(
        from_person="A",
        to_person="B",
        relationship_type=WorkRelationshipType.COLLEAGUE
    )
    assert relationship.bidirectional == True
    assert relationship.strength is None
    assert relationship.created_at is not None

    interaction = Interaction(
        with_person="Test",
        interaction_type=InteractionType.EMAIL
    )
    assert interaction.participants == []
    assert interaction.follow_up_required == False
    assert interaction.date is not None


def test_model_validation_errors():
    """Test model validation errors."""
    # Person requires name
    with pytest.raises(ValidationError):
        Person()

    # WorkRelationship requires from_person, to_person, relationship_type
    with pytest.raises(ValidationError):
        WorkRelationship()

    with pytest.raises(ValidationError):
        WorkRelationship(from_person="A")

    # Interaction requires with_person and interaction_type
    with pytest.raises(ValidationError):
        Interaction()

    with pytest.raises(ValidationError):
        Interaction(with_person="Test")


def test_enum_from_string():
    """Test enum creation from string values."""
    rel_type = WorkRelationshipType("manager")
    assert rel_type == WorkRelationshipType.MANAGER

    comm_pref = CommunicationPreference("email")
    assert comm_pref == CommunicationPreference.EMAIL

    interaction_type = InteractionType("meeting")
    assert interaction_type == InteractionType.MEETING


def test_model_field_validation():
    """Test specific field validation."""
    # Test that datetime fields are properly handled
    person = Person(name="Test")
    assert isinstance(person.created_at, datetime)
    assert isinstance(person.updated_at, datetime)

    # Test that list fields default to empty lists
    assert isinstance(person.expertise_areas, list)

    # Test that dict fields default to empty dicts
    assert isinstance(person.attributes, dict)


def test_relationship_context_validation():
    """Test relationship context field."""
    relationship = WorkRelationship(
        from_person="Alice",
        to_person="Bob",
        relationship_type=WorkRelationshipType.COLLABORATOR,
        context="Working together on Project X"
    )

    assert relationship.context == "Working together on Project X"

    # Test without context
    relationship_no_context = WorkRelationship(
        from_person="Alice",
        to_person="Bob",
        relationship_type=WorkRelationshipType.COLLEAGUE
    )

    assert relationship_no_context.context is None
