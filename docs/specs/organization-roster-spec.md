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
- [Future Developers](#future-developers)
  - [Frontend Concerns](#frontend-concerns)
  - [Backend Concerns](#backend-concerns)


# Descriptions and Sample Data Representation of feature

We have added/modified the following models/Api Routes

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
class Member(BaseModel):
    id: int | None = None
    user_id: int | None = None
    organization_id: int | None = None
    term: str
    year: str | None = None
    description: str | None = None
    isLeader: bool
    position: str | None = "Member"
    major: str | None = None
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
<img width="1314" alt="Screenshot 2024-05-03 at 3 55 04 PM" src="https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/7b32ff16-7acc-4c8b-a057-5e4d27b59fdc">

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

# Future Developers

Development concerns: This section is designed for new developers interested in making future changes to enhance and expand our features. This guide will be split into two sections: Frontend Concerns and Backend Concerns. We want to separate the concerns of the API and backend service layer with the frontend services and Angular layer. If you want to focus on the backend, you should focus on the Backend section, but still familiarize yourself with the major aspects of the Frontend section. Similarly, if you want to focus on the frontend, focus on the Frontend section while familiarizing yourself with the major aspects of the Backend section. Since the two sections are inherently tied to each other, it's important to be familiarized with the overarching aspects of both regardless of your focus. Having a holistic approach to understanding how our features are implemented will be the most effective way of developing more effectively. 

## Frontend Concerns

The Organization Member Roster feature contains 4 components and 2 services. Users can access this feature by routing to the organization details page by clicking on the organization tab on the navigation bar and clicking on any organization's details button. Adding onto the pre-existing structure of the organization details page was a key factor in our ease of development and design choices. Not only does it aid in the UI/UX of this section of the application, but it allows future developers to easily familiarize themselves with the code. 

### Components

#### Organization Roster Component:
<img width="1233" alt="Screenshot 2024-05-02 at 10 32 50 PM" src="https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/91a60122-950d-400b-9357-a0164bf11668">

This component holds a table that displays all of the members of an organization where the default view shows their name and their position. A clickable dropdown shows more information about each member (their major, minor, year, and bio). A registered user is able to see all members of every club and their public information. Leaders of an organization will have a different view that will show an 'Edit Member' button. Clicking this button will navigate the leader to the Edit Member Component. This component has access to the member service that holds business logic to make HTTP Requests to the backend. We decided to have users access this component through a button on the already-existing Organization Details Component. Clicking 'View Full Roster' will navigate the user to the Organization Roster Component. 

#### Organization Application Component:
<img width="1169" alt="Screenshot 2024-05-02 at 10 34 08 PM" src="https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/4ecc7495-8161-424f-9717-5b2734a0291e">

This component holds a form that any user can fill out and submit. This component has access to the applicant service holding the business logic to make HTTP Requests. If an organization is of the 'App' status as seen in the Organization Type Enumeration, users will be able to click an 'Apply' button on the Organization Details Info Card Widget on the Organization Details Component. Routing to the application page and submitting the application will allow for leaders to review said application and accept or reject it in the Organization Applicants Component. 

#### Organization Applicants Component: 
<img width="1219" alt="Screenshot 2024-05-02 at 10 40 06 PM" src="https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/2cec22c3-ffd4-4342-b9e4-daca54a5cd4d">

This component holds a table that displays all pending applicants of an organization. This component has access to the applicant service and the member service that holds business logic to make HTTP Requests. Only the leaders of an organization will have a 'View Pending Applicants' button displayed on the Oragnization Details Info Card Widget on the Organization Details Component. Navigating to the applicants page, a leader will see all of the users who have applied to the organization and will be able to accept or reject applicants via a drop down button. 

#### Edit Member Component
<img width="1219" alt="Screenshot 2024-05-02 at 10 40 51 PM" src="https://github.com/comp423-24s/csxl-final-team-c6/assets/111467809/6aa2027d-314b-45e3-95e9-b82b787418f2">

This component contains a form field and various action buttons to change the state of a member. This component has access to the member service that holds the business logic to update a member in the backend through an HTTP Request. Only the leaders of an organization will be able to view an edit button on the organization roster to access this component. When a leader navigates to this page, it will display the member's current information (position and leadership permissions), a form field to change the member's position, a button to toggle leadership permissions, and a button to remove the member from the organization.

### Services

The two services we introduced are the Member Service and the Applicant Service which can be found in the Organization Folder

#### Member Service

The Member Service introduces 12 new methods:

1. getCurrentTerm: Static method that retrieves the current term.
2. getTerms: Static method that retrieves terms from the last two years.
3. getMembers: Retrieves all members of an organization.
4. getMemberById: Retrieves a single member.
5. getMembersByTerm: Retrieves all members of an organization based on a provided term.
6. getMembersByOrgAndUser: Retrieves a single member associated with an organization and a user.
7. getUserMemberships: Retrieves all members associated with a user.
8. getUserMembershipsByTerm: Retrieves all members associated with a user based on a provided term.
9. addMember: Creates a new member, giving a user membership of an organization.
10. deleteMember: Deletes a member, revokes a user's membership of an organization.
11. updateMember: Updates a member.
12. joinOrganizationWithExistingDetails: Joins an organization and applies existing member metadata to all members already associated with the user of the current term.

These methods are used to create, retrieve, update, and delete members from the backend. This service's purpose is to interact with members in the backend. 

#### Applicant Service

The Applicant Service introduces 6 new methods:

1. getApplicants: Retrieves all applicants of an organization.
2. getApplicant: Retrieves a single applicant.
3. getUserApplications: Retrieves all applications a user has submitted.
4. createApplicant: Creates an applicant when an application is submitted.
5. updateApplicant: Updates the status of the applicant (Accepted, Rejected, or Pending).
6. removeApplicant: Deletes the applicant. 

These methods are used to create, retrieve, update, and delete applicants from the backend. This service's purpose is to interact with applicants in the backend. 

## Backend Concerns

For this feature, the backend focuses on relating users and organizations through members and applications. To properly understand the entirety of the backend functionality, we recommend starting from the top and moving down in alignment with this guide. We will start with the API layer, move down to the service layer that queries the database, and end with the entities that define the structure of our data in the persistent database. 

### 1) API Layer

It is recommended that you review the code in `backend/api/members`, `backend/api/applicants`, the Member Model in `backend/models/member`, and the Applicant Model in `backend/models/applicant`. Each of our API methods make use of the Organization Service, User Service, User Model, and Organization Model. It is also recommended to familiarize yourself with each of these files to have a better understanding of how the Member API calls make use of already-existing services and models. This is the first layer that is interacting with the frontend through the frontend services. Understanding this layer first is key to having a holistic understanding of the system. 

### Members API: In the `backend/api/members` file we created several routes:

```py3
@api.get("/{slug}", response_model=list[MemberDetails], tags=["Members"])
def get_organization_members(
    slug: str,
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> list[MemberDetails]:

    organization = organization_service.get_by_slug(slug)
    return member_service.get_members_of_organization(organization)


@api.get("/{slug}/{term}", response_model=list[MemberDetails], tags=["Members"])
def get_organization_members_by_term(
    slug: str,
    term: str,
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> list[MemberDetails]:

    organization = organization_service.get_by_slug(slug)
    return member_service.get_members_of_organization_by_term(organization, term)


@api.get("/{slug}/user/{user_id}", response_model=MemberDetails, tags=["Members"])
def get_member_by_user_and_org(
    slug: str,
    user_id: int,
    organization_service: OrganizationService = Depends(),
    user_service: UserService = Depends(),
    member_service: MemberService = Depends(),
) -> MemberDetails:

    organization = organization_service.get_by_slug(slug)
    subject = user_service.get_by_id(user_id)
    return member_service.get_member_by_user_and_org(subject, organization)


@api.get("/id/id/{id}", response_model=MemberDetails, tags=["Members"])
def get_member_by_id(
    id: int, member_service: MemberService = Depends()
) -> MemberDetails:

    return member_service.get_member_by_id(id)


@api.get("/user/memberships/{user_id}", response_model=list[MemberDetails], tags=["Members"])
def get_user_memberships(
    user_id: int,
    member_service: MemberService = Depends(),
    user_service: UserService = Depends(),
) -> list[MemberDetails]:

    user = user_service.get_by_id(user_id)
    return member_service.get_user_memberships(user)


@api.get("/user/memberships/{user_id}/{term}", response_model=list[MemberDetails], tags=["Members"])
def get_user_memberships_by_term(
    user_id: int,
    term: str,
    member_service: MemberService = Depends(),
    user_service: UserService = Depends(),
) -> list[MemberDetails]:

    user = user_service.get_by_id(user_id)
    return member_service.get_user_memberships_by_term(user, term)


@api.post("/{slug}/create/{user_id}/{term}", response_model=MemberDetails, tags=["Members"])
def add_member(
    slug: str,
    user_id: int,
    term: str,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> MemberDetails:

    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.add_member(user, organization, term)


@api.delete("/{slug}/delete/{user_id}/{term}", response_model=None, tags=["Members"])
def remove_member(
    slug: str,
    user_id: int,
    term: str,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
):
    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.remove_member(user, organization, term)


@api.put("", responses={404: {"model": None}}, response_model=Member, tags=["Members"])
def update_member(
  member: Member,
  member_service: MemberService = Depends()
) -> Member:

    return member_service.update_member(member)
```

The `get_organization_members()` method takes in an organzation's slug as an argument. The slug is used to determine which organization we are grabbing the members of. 

The `get_organization_members_by_term()` method takes in an organization's slug and a term as arguments. The slug is used to determine the organization we are grabbing the members of while the term specifies which year and semester we are grabbing the members from.

The `get_member_by_user_and_org()` method takes in an organization's slug and a user's id as arguments. As you will see below we also have a method that gets the user memberships as a list. Here, we wanted to create a version that only grabs a single member to check if the user is already a member of an organization. Rather than having to go through an entire list, we can just check if any instance exists, and do the according functionality in the frontend.

The `get_member_by_id()` method takes in a member's id as an argument. The unique id is used to specific exactly which member is being retrieved. This method is primarily used for the Edit Member Component in the frontend to update members because the id will appear in the URL where we will be able to grab it and pass through an HTTP Request in the frontend.

The `get_user_memberships()` method takes in a user's id as an argument. This is used to grab the user we want to pass through to the member service. 

The `get_user_memberships()` method takes in a user's id and a term as arguments. This is used to grab the user we want to pass through to the member service and the term specifies which year and semester we are grabbing the member from. 

The `add_member()` method takes in an organization's slug, a user's id, and a term as arguments. These are used to pass user and organization models to the member service while specifying which term to add the member to.

The `remove_member()` method takes in an organization's slug, a user's id, and a term as arguments. These are used to pass user and organization models to the member service while specifying which term to delete the member from.

The `update_member()` method takes in a member model that is passed to the member service to be updated. 

### Applicants API: In the `backend/api/applicants` file we created several routes:

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


@api.get("/applications/{user_id}", response_model=list[ApplicantDetails], tags=["Applicants"])
def get_user_applications(
    user_id: int,
    application_service: ApplicantService = Depends(),
    user_service: UserService = Depends()
) -> list[ApplicantDetails]:

    user = user_service.get_by_id(user_id)
    return application_service.get_user_applications(user)


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

The `get_organization_applicants()` method takes in an organzation's slug as an argument. The slug is used to determine which organization we are grabbing the members of. 

The `get_applicant_by_id()` method takes in an applicant's id as an argument. The unique id is used to specific exactly which applicant is being retrieved. 

The `get_user_applications()` method takes in a user's id as an argument which is used to identify the user we want the applications of.

The `new_applicant()` method takes in an organization's slug, a user model, and an applicant model. These are used to pass applicant, user, and organization models to the member service.

The `update_applicant()` method takes in an id and an applicant model as arguments. 

The `delete_applicant()` method takes in an applicant's id and a user model as arguments. These are used to pass user and applicant models to the member service.

### 2) Member and Applicant Service

While reading through the previous section, you should have noticed that each of the API methods either returns a method call, or ends in a method call from the respective service. Aside from the `get_current_term()` method in the `backend/services/member` file, every method written in the member and applicant service corresponds to the similarly named API call. The service uses a SQLAlchemy Session to query and alter the database based on what was passed through to us in the API methods. Each service method creates a SQLAlchemy Entity by querying the database using what was given to us from the API's arguments, uses this entity to interact with the database, then turns the entity back into a Pydantic Model (if applicable) so the rest of the backend can use it. Aside from the small paragraphs below, there isn't anything that separates our services from the rest of the codebase that you need to know to effectively extend or improve our feature. 

One important aspect of our feature that you may be asking yourself questions about is how we deal with the term, and more specifically, how we grab the current term. Each instance of a member is associated with a term, and every time we create a new member or update an existing member, the desired outcome is to ensure the member is associated with whatever term it is in real time. The `get_current_term()` method in `backend/services/member` uses the Python Datetime Module to grab the current term from real time. Using the return value of this method, we can ensure that members from previous terms remain unchanged.

Another important aspect of our Member Service worth noting can be seen in the `get_member_by_user_and_org()` method. On line 150, we see that if the `subject.id == 1` we return a blank leader model that represents the root user. We did not implement permissions in line with the rest of the codebase due to complications that will be mentioned in the Future Considerations portion of this document. We found a simple way around these complications that will eventually need to change, but as of now, every time we are checking if a user is a member of the organization's page they are on, we return a "fake" member that has leader permissions when logged in an Rhonda. We hardcoded the id being equal to one, but this may need to change depending on what the main branch uses for the root user. Essentially, this is a quick and easy patch to a more complex problem that we wil talk about later in the document, but it is worth mentioning here to establish one of the ways we approach the root user having all permissions available.

### 3) Models

We added four new models to implement our feature which are the Member, MemberDetails, Applicant, and ApplicantDetails models. While we briefly discuss these models below it is important to review the Organization and User models, as they are frequently used throughout our feature's code, and the rest of the codebase.

#### Member and MemberDetails
```py3
class Member(BaseModel):
    id: int | None = None
    user_id: int | None = None
    organization_id: int | None = None
    term: str
    year: str | None = None
    description: str | None = None
    isLeader: bool
    position: str | None = "Member"
    major: str | None = None
    minor: str | None = None

class MemberDetails(Member):
    user: User
    organization: Organization
```

The Member model above follows the same format and use of most other models seen throughout the codebase. In particular, we make use of a MemberDetails model that inherits from the Member model to store a User and Organization model that corresponds to the given Member model. We want to have direct access to these because rather than querying the database using the user's and organization's id, we can store an instance of them knowing we will use their attributes throughout the frontend and backend. Instead of storing these models directly in the Member model, we move them to a details model to prevent circular imports in the MemberEntity.

#### Applicant and ApplicantDetails
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

class ApplicantDetails(Applicant):
    user: User
    organization: Organization
```

The reasoning for the Applicant and ApplicantDetails models is exactly the same as what you read above. One thing to notice is the ApplicantStatus enumeration. This is used in both the backend and frontend to indicate whether the application is pending, accepted, or rejected. Nothing special is being done here, but it is a difference worth noting from the Member model above.


### 4) Entities 

While reading through this section of the document it is advised to familiarize yourself with the `backend/entities/member_entity` and `backend/entities/applicant_entity` files. While we won't go over SQLAlchemy Entities in detail here, refer to the `backend/docs/sqlalchemy` files to understand the basics of how they are used throughout the codebase. You should also familiarize yourself with the `backend/entities/organization_entity` and `backend/entities/user_entity` files. The User and Organization Entity were vital in integrating our feature into this codebase and you will not be able to further develop our feature without a strong understanding of how these entities work and how they will ultimately be related. 

#### Member Entity

After reading the documentation on SQLAlchemy Entities and reviewing the related files, you will notice that we set the Member Entity up to act as an association table between Users and Organizations. This is because Users and Organizations have a many-to-many relationship where a user can be a part of many organizations while an organization has many members (users) associated with it. 

```py3
user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
user: Mapped["UserEntity"] = relationship(back_populates="members")

organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), primary_key=True)
organization: Mapped["OrganizationEntity"] = relationship(back_populates="members")
```

The code above is what defines our many-to-many relationship. 

Instead of the Member Entity being a simple association table, we also wanted members to have specific attributes that aren't found anywhere else in the codebase. This is why you'll see us declare other fields such as "year", "description", "major", etc. These represent the metadata we want members to have alongside the relationship between two entities they establish.

```py3
def to_model(self) -> Member:
        return Member(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            term=self.term,
            year=self.year,
            description=self.description,
            isLeader=self.isLeader,
            position=self.position,
            major=self.major,
            minor=self.minor,
        )

    def to_details_model(self) -> MemberDetails:
        return MemberDetails(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            year=self.year,
            term=self.term,
            description=self.description,
            isLeader=self.isLeader,
            position=self.position,
            major=self.major,
            minor=self.minor,
            user=self.user.to_model(),
            organization=self.organization.to_model(),
        )

    @classmethod
    def from_model(cls, model: Member) -> Self:
        return cls(
            id=model.id,
            user_id=model.user_id,
            organization_id=model.organization_id,
            term=model.term,
            year=model.year,
            description=model.description,
            isLeader=model.isLeader,
            position=model.position,
            major=model.major,
            minor=model.minor,
        )
```

You'll also notice that we define class methods that allow us to translate our Member Entities into Member Pydantic Models. We included `to_details_model()` function because we want direct access to the User and Organization Models that are associated with the Member in both the frontend and backed. This choice allows us to access all of the associated user's and organization's attributes directly rather than writing excessive calls in the frontend. 

#### Applicant Entity

Similarly, the Applicant Entity acts as an association table between Users and Organizations. We chose to make an entity for the applications because we want to store the application until the leaders of an organization decide to run through an accept them. We also want to display an application's status to the user that submitted it and have them persist beyond acceptance or rejection.

```py3
user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
user: Mapped["UserEntity"] = relationship(back_populates="applicants")

organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
organization: Mapped["OrganizationEntity"] = relationship(back_populates="applicants")
```

The code above is what defines our many-to-many relationship. 

Again, despite the fact that the Applicant Entity serves as an association table, we want to store information that the user puts into the application to display to the leaders on a separate page. 

```py3
def to_model(self) -> ApplicantDetails:
        return ApplicantDetails(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            status=self.status,
            name=self.name,
            email=self.email,
            major=self.major,
            minor=self.minor,
            year=self.year,
            pronouns=self.pronouns,
            interest=self.interest,
            user=self.user.to_model(),
            organization=self.organization.to_model(),
        )

    @classmethod
    def from_model(cls, model: Applicant) -> Self:
        return cls(
            id=model.id,
            user_id=model.user_id,
            organization_id=model.organization_id,
            status=model.status,
            name=model.name,
            email=model.email,
            major=model.major,
            minor=model.minor,
            year=model.year,
            pronouns=model.pronouns,
            interest=model.interest,
        )
```

Seen in the code snippet above, we chose to not write a separate to details model function because we aren't using an Applicant without it being in the form of the ApplicantDetails.

## Future Considerations

### Integrate organization permissions in with the existing permission system

  - Implement group-based permissions that allow for bulk setting of access rights according to the role within the organization.

### Add ability to post member-only information
  
  - Create a secure, members-only section on the website where members only content can be shared.
  - Implement authentication and authorization checks to ensure that only logged-in members with the appropriate permissions can view member only content.

### Add ability for organizations to post a link for external applications if they want
 
  - Allow organizations to integrate external application processes by providing a feature to add customizable application links on their detials page.
