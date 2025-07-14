"""Tests for data models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.database.models import (ContactMethod, Interaction, InteractionType,
                                 Person, RelationshipType, WorkRelationship)


def test_person_model():
    """Test Person model validation and serialization."""
    person = Person(
        name="John Doe",
        email="john.doe@company.com",
        department="Engineering",
        role="Senior Developer",
        skills=["Python", "React", "AWS"],
        location="New York"
    )

    assert person.name == "John Doe"
    assert person.email == "john.doe@company.com"
    assert person.department == "Engineering"
    assert person.role == "Senior Developer"
    assert "Python" in person.skills
    assert person.location == "New York"


def test_person_email_validation():
    """Test email validation in Person model."""
    # Valid email
    person = Person(
        name="John Doe",
        email="john.doe@company.com",
        department="Engineering",
        role="Developer"
    )
    assert person.email == "john.doe@company.com"

    # Invalid email should raise validation error
    with pytest.raises(ValidationError):
        Person(
            name="John Doe",
            email="invalid-email",
            department="Engineering",
            role="Developer"
        )


def test_work_relationship_model():
    """Test WorkRelationship model."""
    relationship = WorkRelationship(
        person1_email="john@company.com",
        person2_email="jane@company.com",
        relationship_type=RelationshipType.COLLABORATOR,
        strength=0.8,
        project="Project Alpha",
        start_date=datetime(2024, 1, 1)
    )

    assert relationship.person1_email == "john@company.com"
    assert relationship.person2_email == "jane@company.com"
    assert relationship.relationship_type == RelationshipType.COLLABORATOR
    assert relationship.strength == 0.8
    assert relationship.project == "Project Alpha"


def test_relationship_strength_validation():
    """Test relationship strength validation (0.0 to 1.0)."""
    # Valid strength
    relationship = WorkRelationship(
        person1_email="john@company.com",
        person2_email="jane@company.com",
        relationship_type=RelationshipType.PEER,
        strength=0.5
    )
    assert relationship.strength == 0.5

    # Invalid strength (negative)
    with pytest.raises(ValidationError):
        WorkRelationship(
            person1_email="john@company.com",
            person2_email="jane@company.com",
            relationship_type=RelationshipType.PEER,
            strength=-0.1
        )

    # Invalid strength (greater than 1)
    with pytest.raises(ValidationError):
        WorkRelationship(
            person1_email="john@company.com",
            person2_email="jane@company.com",
            relationship_type=RelationshipType.PEER,
            strength=1.1
        )


def test_interaction_model():
    """Test Interaction model."""
    interaction = Interaction(
        person1_email="john@company.com",
        person2_email="jane@company.com",
        interaction_type=InteractionType.MEETING,
        contact_method=ContactMethod.IN_PERSON,
        timestamp=datetime(2024, 1, 15, 10, 30),
        duration_minutes=60,
        topic="Project discussion",
        context="Sprint planning meeting"
    )

    assert interaction.person1_email == "john@company.com"
    assert interaction.person2_email == "jane@company.com"
    assert interaction.interaction_type == InteractionType.MEETING
    assert interaction.contact_method == ContactMethod.IN_PERSON
    assert interaction.duration_minutes == 60
    assert interaction.topic == "Project discussion"


def test_interaction_duration_validation():
    """Test interaction duration validation (positive integer)."""
    # Valid duration
    interaction = Interaction(
        person1_email="john@company.com",
        person2_email="jane@company.com",
        interaction_type=InteractionType.EMAIL,
        duration_minutes=30
    )
    assert interaction.duration_minutes == 30

    # Invalid duration (negative)
    with pytest.raises(ValidationError):
        Interaction(
            person1_email="john@company.com",
            person2_email="jane@company.com",
            interaction_type=InteractionType.EMAIL,
            duration_minutes=-10
        )


def test_enum_values():
    """Test enum values are correctly defined."""
    # RelationshipType
    assert RelationshipType.MANAGER == "manager"
    assert RelationshipType.DIRECT_REPORT == "direct_report"
    assert RelationshipType.PEER == "peer"
    assert RelationshipType.COLLABORATOR == "collaborator"
    assert RelationshipType.MENTOR == "mentor"
    assert RelationshipType.MENTEE == "mentee"

    # InteractionType
    assert InteractionType.MEETING == "meeting"
    assert InteractionType.EMAIL == "email"
    assert InteractionType.CHAT == "chat"
    assert InteractionType.CALL == "call"
    assert InteractionType.COLLABORATION == "collaboration"

    # ContactMethod
    assert ContactMethod.IN_PERSON == "in_person"
    assert ContactMethod.VIDEO_CALL == "video_call"
    assert ContactMethod.PHONE_CALL == "phone_call"
    assert ContactMethod.EMAIL == "email"
    assert ContactMethod.CHAT == "chat"


def test_model_serialization():
    """Test model serialization to dict."""
    person = Person(
        name="John Doe",
        email="john@company.com",
        department="Engineering",
        role="Developer",
        skills=["Python", "JavaScript"]
    )

    person_dict = person.model_dump()

    assert person_dict["name"] == "John Doe"
    assert person_dict["email"] == "john@company.com"
    assert person_dict["department"] == "Engineering"
    assert person_dict["skills"] == ["Python", "JavaScript"]

    # Test with exclude
    person_dict_minimal = person.model_dump(exclude={"skills", "location"})
    assert "skills" not in person_dict_minimal
    assert "location" not in person_dict_minimal
    assert "name" in person_dict_minimal
