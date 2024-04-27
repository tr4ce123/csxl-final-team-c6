# Organization Roster Technical Specification

This document contains the technical specifications, this feature adds new API routes, new database tables, and new frontend components to the organization

# Authors
- [Connor Vines](https://github.com/vinesconnor)
- [Gregory Glasby](https://github.com/tr4ce123)
- [Luis Villa](https://github.com/vluis26)
- [Adrian Lanier](https://github.com/adlanier)

# Table of Contents
- [Descriptions and Sample Data Representation of Feature](#descriptions-and-sample-data-representation-of-feature)
  - [Models](#0-organization-type)
  - [Services](#member-service)
  - [API Routes](#api-routes)
- [Underlying Database/Entity-Level Representation Decisions](#underlying-databaseentity-level-representation-decisions)
- [Technical and User Experience Design Choice](#technical-and-user-experience-design-choice)
- [Development Concerns](#development-concerns)


# Descriptions and Sample Data Representation of feature

We have added/modified the following models/Api Routes (current stories done)

## 0. Organization Type
Before:
```py3
class Organization(BaseModel):

    id: int | None = None
    name: str
    shorthand: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    public: bool
```

After:
```py3
class OrganizationType(Enum):
  OPEN = 0
  APP = 1
  CLOSED = 2

class Organization(BaseModel):

    id: int | None = None
    name: str
    shorthand: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    public: bool
    org_type: OrganizationType
```
Created an OrganizationType class in order to determine whether a certain organization is Open, Application only, or Closed. 

## 1. Member
```py3
class MemberYear(Enum):
    FRESHMAN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4
    FIFTH_YEAR = 5
    GRAD = 6

class Member(BaseModel):
    id: int | None = None
    user_id: int | None = None
    organization_id: int | None = None
    term: str
    year: MemberYear
    description: str | None = None
    isLeader: bool
    position: str | None = "Member"
    major: str
    minor: str | None = None
```
Pydantic model to represent a member without user and organization to avoid circular dependencies. Created MemberYear enum to represent a member's current academic status.


## 2. MemberDetails
```py3
class MemberDetails(Member):
    user: User
    organization: Organization
```
Pydantic model to represent a Member. This model is based on the `MemberEntity` model, which defines the shape of the `Member` database in the PostgreSQL database.

## 3. Applicant
```py3
class ApplicantStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = -1


class Applicant(BaseModel):
    id: int
    user_id: int | None = None
    organization_id: int | None = None
    status: ApplicantStatus
    name: str
    email: str
    major: str
    minor: str | None = None
    year: str
    pronouns: str
    interest: str
```
Created an ApplicantStatus in order to distinguish in what part of the application the student is currently in. The Applicant class lists the parts needed for an application. This model is based on the `MemberEntity` model, which defines the shape of the `Member` database in the PostgreSQL database

## 4. Applicant Details

```py3
class ApplicantDetails(Applicant):
    user: User
    organization: Organization
```
Pydantic model to represent an Applicant. This model is based on the `ApplicantEntity` model, which defines the shape of the `Applicant` database in the PostgreSQL database.

## API Routes
The Organization Roster feature adds 13 new API routes to handle CRUD operations.
Member and Applicant APIs.
![image](https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/0ea559ad-9cd5-4170-808e-58bf76e1511f)
| Table Name        | Resource              | Description                                                |
| ----------------- | ------------------- | ---------------------------------------------------------- |
| `members.get`          | `"/{slug}"`      | Get the members of a specific organization.   |
| `members.get`          | `"/{slug}/{term}"`      | Get the members of a specific organization by term.   |
| `members.get`       | `"/id/id/{id}"`   | Get a member by its ID.                            |
| `members.get`       | `"/user/memberships/{user_id}"`   | Get all members associated with a specific user.                            |
| `members.get`       | `"/user/memberships/{user_id}/{term}"`   | Get all members associated with a specific user by term.   |
| `members.post`       | `"/{slug}/create/{user_id}/{term}"`   | Have a user become a member of an organization during the current term.        |
| `members.delete`       | `"/{slug}/delete/{user_id}/{term}"`   | Remove a member from an organization of a specific term.                  |
| `members.put`       | `""`   | Updates a member.                            |
| `applicants.get`       | `"/{slug}"`   | Get the applicants of a specific organization.                            |
| `applicants.post`       | `"/{slug}"`   | Have a user become an applicant of an organization.                            |
| `applicants.get`       | `"/id/{id}"`   | Get an applicant by its ID.                            |
| `applicants.put`       | `"/{id}"`   | Updates an applicant.                            |
| `applicant.delete`       | `"/{id}"`   | Remove an applicant from an organization.                            |

# Underlying database/entity-level representation decisions

The Organization Roster Feature adds two new database tables and entities. They are as follows:

| Table Name        | Entity              | Description                                                |
| ----------------- | ------------------- | ---------------------------------------------------------- |
| `member`          | `MemberEntity`      | Stores meta-data about membership to given organization.   |
| `applicant`       | `ApplicantEntity`   | Stores application form fields.                            |

While we would like to create a visual schema for the final document, we will just explain their relationships textually for now.

The `member` table has a one-to-many relationship with both the `user` and `organization` tables. We settled on this because any given user may be a member of many organizations, and similarly, any organization will likely have many members. This table essentially serves as an association table between the `user` and `organization` tables and includes useful meta-data like the member's position, permissions, and information about themselves they want to make public to the organization.

The setup of the `applicant` table is very similar to that of the `member` table. It acts as an association table between `user` and `organization` maintaining one-to-many relationships with both. The fields of this table directly encapsulate the application form fields on the front-end, making its design relatively straightforward.

# Technical and User Experience Design Choice

## 1. Accept and Reject Applicant Back-end Behavior

**Deleting Reviewed Applications:**
| Pros                                                                   | Cons                                                                                                   |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| This is easier to implement on the backend.                            | Users would get no indication that their application has been processed besides being a member or not. |
| This allows users to reapply to organizations they were rejected from. | Organizations may want to maintain past applications for future use.                                   |
| This prevents database clutter as no erroneous information is stored.  | Lost applications could limit or impact the transparency behind the leader's decision.                 |

**Maintaining Reviewed Applications:**
| Pros                                                                                              | Cons                                                                                             |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Preserves past records of applications.                                                           | Required adding organization status field (enum) to organization entity and models.              |
| Allows future work to display past applications and their statuses to a user.                     | Prevents users from reapplying to the same organization if rejected (unless future work-arounds) |
| Enhances user experience because their applications do not just disappear from their prospective. | Could potentially clutter the database if not maintained properly.                               |

**Decision Made and Reasoning:** Ultimately, we decided to add the status field to the applicant table and maintain past applications. This decision was based on the belief that retaining past applications would provide more flexibility and functionality in the long term. It allows us to build future features that could display a user's application history and their outcomes. Furthermore, we believed the user case of seeing an application "disappear" from their prospective with no confirmation of a rejection would be heavily disliked. The main trade-off with this approach is that users cannot reapply to an organization that they have been rejected from, unless we implement additional logic to handle these cases.

## 2. Organization Status Display
**Challenge:** When a user views the organization page, we wanted them to be able to tell an organization's status (Open, Application-Based, Closed) without having to visit the organization's details page. This presented a decision with trade-offs between asthetics and interpretability.

**Textual Representation: Open, Application, Closed**
| Pros                                                                   | Cons                                                                                                                       |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Extremely easy for any user to understand.                             | Looks very primitive.                                                                                                      |
| Simpler implementation.                                                | Organizations with different statuses looked irregular and inconsistent.                                                   |
|                                                                        | Application is a very large word to display, but the alternative 'App' may not be interpretable or intuitive to all users. |

**Visual Representation: Green, Yellow, Red**
| Pros                                                                   | Cons                                                                                                                       |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Looks very clean.                                                      | More complex CSS implementation                                                                                            |
| Clutters the organization cards less.                                  | The meaning of color codes may not be intuitive to all users.     |

**Decision Made and Reasoning:** Initially, we chose textual representations due to their clarity. However, during internal use, we favored the aesthetically pleasing color icons. As time progressed, we grew attached to the color icons and looked for alternative methods. We came to the decision to merge the two approaches. Taking inspiration from the descriptions on the organization cards, we changed the icons so that colors are displayed, but hovering over the icons shows the original, textual representation. We think that this is a good middleground. It maintains the slick and clean work of the website without cluttering the organization cards. We believe the hover-over feature to adequately address any confusions, as users uncertain about the colors will likely seek out the text explanation. This hybrid approach effectively balances beauty with functionailty, offering the best of both worlds.

# Development concerns

Development concerns: This section is designed for new developers interested in making future changes to enhance and expand our features. This guide will be split into two sections: Frontend Concerns and Backend Concerns. We want to separate the concerns of the API and backend service layer with the frontend services and Angular layer. If you want to focus on the backend, you should focus on the Backend section, but still familiarize yourself with the major aspects of the Frontend section. Similarly, if you want to focus on the frontend, focus on the Frontend section while familiarizing yourself with the major aspects of the Backend section. Since the two sections are inherently tied to each other, it's important to be familiarized with the overarching aspects of both regardless of your focus. Having a holistic approach to understanding how our features are implemented will be the most effective way of developing more effectively. 

## Frontend Concerns

The Organization Member Roster feature contains 3 components and 1 service. Users can access this feature by routing to the organization details page by clicking on the organization tab on the navigation bar and clicking on any organization's details button. Adding onto the pre-existing structure of the organization details page was a key factor in our ease of development and design choices. Not only does it aid in the UI/UX of this section of the application, but it allows future developers to easily familiarize themselves with the code. 

### Components

#### Organization Roster Component:

This component holds a table that displays all of the members of an organization where the default view shows their name and their position. A clickable dropdown shows more information about each member (their major, minor, year, and bio). A registered user is able to see all members of every club and their public information. This component has access to the member service that holds business logic to make HTTP Requests to the backend. We decided to have users access this component through a button on the already-existing Organization Details Component. Clicking 'View Full Roster' will navigate the user to the Organization Roster Component. Leaders of an organization will have a different view that will show an 'Edit Member' button. Clicking this button will navigate the leader to the Edit Member Component.


#### Organization Application Component:

This component holds a form that any user can fill out and submit. This component has access to the applicant service holding the business logic to make HTTP Requests. If an organization is of the 'App' status as seen in the Organization Type Enumeration, users will be able to click an 'Apply' button on the Organization Details Info Card Widget on the Organization Details Component. Routing to the application page and submitting the application will allow for leaders to review said application and accept or reject it in the Organization Applicants Component. 

#### Organization Applicants Component: 

This component holds a table that displays all pending applicants of an organization. This component has access to the applicant service and the member service that holds business logic to make HTTP Requests. Only the leaders of an organization will have a 'View Pending Applicants' button displayed on the Oragnization Details Info Card Widget on the Organization Details Component. Navigating to the applicants page, a leader will see all of the users who have applied to the organization and will be able to accept or reject applicants via a drop down button. 

#### TODO: Edit Member Component

### Services

The two services we introduced are the Member Service and the Applicant Service which can be found in the Organization Folder

#### Member Service

The Member Service introduces 3 new methods:

1. getMembers: Retrieves all members of an organization.
2. addMember: Creates a new member object, giving a user membeership of an organization.
3. deleteMember: Deletes a member object, revokes a users membership of an organization.

These methods are used to create and delete members with the backend. This service's purpose is to interact with members in the backend. 

#### Applicant Service

The Member Service introduces 11 new methods:

1. getCurrentTerm: Static method that retrieves the current term.
3. getMembers: Retrieves all members of an organization.
4. getMemberById: Retrieves a single member.
5. getMembersByTerm: Retrieves all members of an organization based on a provided term.
6. getUserMemberships: Retrieves all members associated with a user.
7. getUserMembershipsByTerm: Retrieves all members associated with a user based on a provided term.
8. addMember: Creates a new member, giving a user membership of an organization.
9. deleteMember: Deletes a member, revokes a user's membership of an organization.
10. updateMember: Updates a member.
11. joinOrganizationWithExistingDetails: Joins an organization and applies existing member metadata to all members already associated with the user of the current term.

These methods are used to create and delete members with the backend. This service's purpose is to interact with members in the backend. 

The Applicant Service introduces 5 new methods:

1. getApplicants: Retrieves all applicants of an organization.
2. getApplicant: Retrieves a single applicant.
3. createApplicant: Creates an applicant when an application is submitted.
4. updateApplicant: Updates the status of the applicant (Accepted, Rejected, or Pending).
5. removeApplicant: Deletes the applicant. 

These methods are used to create, retrieve, update, and delete applicants with the backend. This service's purpose is to interact with applicants in the backend. 

## Backend Concerns

For this feature, the backend focuses on relating users and organizations through members and applications. To properly understand the entirety of the backend functionality, we recommend starting from the top and moving down in alignment with this guide. We will start with the API layer, move down to the service layer that queries the database, and end with the entities that define the structure of our data in the persistent database. 

### API Layer

It is recommended that you review the code in `backend/api/members`, `backend/api/applicants`, and the Member Model in `backend/models/member`. Each of our API methods make use of the Organization Service, User Service, User Model, and Organization Model. It is also recommended to familiarize yourself with each of these files to have a better understanding of how the Member API calls make use of already-existing services and models. This is the first layer that is interacting with the frontend through the frontend services. Understanding this layer first is key to having a holistic understanding of the system. 

#### In the `backend/api/members` file we created the following routes: 

```py3
@api.get("/{slug}", response_model=list[MemberDetails], tags=["Members"])
def get_organization_members(
    slug: str,
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> list[MemberDetails]:
    organization = organization_service.get_by_slug(slug)
    return member_service.get_members_of_organization(organization)

@api.post("/{slug}/create/{user_id}", response_model=MemberDetails, tags=["Members"])
def add_member(
    slug: str,
    user_id: int,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> MemberDetails:
    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.add_member(user, organization)

@api.delete("/{slug}/delete/{user_id}", response_model=None, tags=["Members"])
def remove_member(
    slug: str,
    user_id: int,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
):
    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.remove_member(user, organization)
```

The `get_organization_members()` method takes in an organzation's slug as an argument. The slug is used to determine which organization we are grabbing the members of. 

The `add_member()` method takes in an organization's slug and a user's id as arguments. These are used to pass user and organization models to the Member Service.

The `remove_member()` method takes in an organization's slug and a user's id as arguments.

#### In the `backend/api/applicants` file we created the following routes: 

```py3
@api.get("/{slug}", response_model=list[ApplicantDetails], tags=["Applicants"])
def get_organization_applicants(
    slug: str,
    organization_service: OrganizationService = Depends(),
    application_service: ApplicantService = Depends(),
) -> list[ApplicantDetails]:

    organization = organization_service.get_by_slug(slug)
    return application_service.get_applicants_of_organization(organization)


@api.get("/id/{id}", response_model=ApplicantDetails, tags=["Applicants"])
def get_organization_applicants_by_id(
    id: int,
    application_service: ApplicantService = Depends(),
) -> ApplicantDetails:

    return application_service.get_applicant_by_id(id)


@api.post("/{slug}", response_model=ApplicantDetails, tags=["Applicants"])
def new_applicant(
    slug: str,
    application: Applicant,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    applicant_service: ApplicantService = Depends(),
) -> ApplicantDetails:

    organization = organization_service.get_by_slug(slug)
    return applicant_service.add_applicant_of_organization(
        subject, organization, application
    )


@api.put("/{id}", response_model=ApplicantDetails, tags=["Applicants"])
def update_applicant(
    id: int, application: Applicant, applicant_service: ApplicantService = Depends()
):
    return applicant_service.update_applicant_of_organization(id, application)


@api.delete("/{id}", response_model=None, tags=["Applicants"])
def delete_applicant(
    id: int,
    subject: User = Depends(registered_user),
    applicant_service: ApplicantService = Depends(),
):
    applicant_service.remove_applicant_of_organization(subject, id)
```
TODO: Briefly explain each method

### TODO: Member Service

### TODO: Applicant Service

### TODO: Models

### TODO: Entities
