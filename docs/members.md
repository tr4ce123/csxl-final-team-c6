# Student Organization Roster Management and Members-only Features

**Team C6 Members:** [Luis Villa](https://github.com/vluis26), [Gregory Glasby](https://github.com/tr4ce123), [Adrian Lanier](https://github.com/adlanier), [Connor Vines](https://github.com/vinesconnor)

## Overview

As of now, the Student Organizations are simply listed with links to their website (if they have one), their socials, and public events. Heel Life or an organization’s own management system is where most organizations would be managing their membership relationships. This feature would establish these relationships within the CSXL website and database. This feature will enable clubs to have leadership positions or regular membership status assigned to the appropriate students. Organization leaders will be allowed to accept and reject requests to join, and once a student has been registered, they will have access to that Organization’s member-only events, information, etc. Leaders can also choose to be open to all users rather than using an application or a request to join.

## Key Personas

1. **Sally Student** - I want to be able to view "public" organization details and events, and I want to be able to apply for Organizations on their respective pages so I can gain access to their member only features.
2. **Mark Member** - I want to be able to view member-only information about my organization as well as the member list so I can connect with other people.
3. **Larry Leader** - I want to be able to manage my organization: its settings, information, and members to run my organization in the best way possible.
4. **Ronda Root** - I want to be able to manage and monitor all organizations, their member lists, and their member-only information to ensure a safe environment on the site.

## User Stories

- As **Sally Student**, I would like to view active organizations and have the opportunity to apply/join the ones that I am interested in so I can be more involved in campus life.
- As **Mark Member**, I would like to view the members and leaders in my organization so I can connect with my peers.
- As **Mark Member**, I would like to view the member only events for my organization to take advantage of the benefits of being a member.
- As **Larry Leader**, I want to be able to remove members from my organization that violate our rules to maintain a safe environment for our members.
- As **Larry Leader**, I want to be able to post member-only information (in markdown), like links to Slack or GroupMe, and events so my members know where to access important information or events.
- As **Larry Leader**, I want to be able to set my organization to different types like open, closed, or application-based and review pending applications if necessary, so I can control who is and is not a member.
- As **Larry Leader**, I want to be able to give certain members privileges and titles to delegate the responsibilities of the organization.
- As **Rhonda Root**, I want to be able to do everything on the site relating to organizations (essentially, leader permissions for every organization) so I can maintain a safe environment on the site.

## Wireframes

All wireframes and the full user flow of the Organization Roster Management and Members-only Features function can be found on [Figma](https://www.figma.com/file/Vs8DZ3gfeBCFeZT9nfaBKU/COMP-423-Project-Mockup?type=whiteboard&node-id=0%3A1&t=IuLtKhFtyuUvhKp9-1).

### Sally Student

As **Sally Student**, I want to be able to join or apply to new organizations via the Join Organization Button as seen in "Open Org" and "Application/Request Org" in the mockup. If I click the Request to Join button, I will be able to fill out the application on a new form page (Request to Join Form). I also will not be able to join clubs marked "Closed" (Closed Org).

As **Sally Student**, I want to be able to view the roster of any given organization via the View Full Roster button to see if I know anyone in the club (Roster Page). I will also be able to see the leaders listed on the Organization Details page.

### Member Mark

As **Member Mark**, I want to be able to leave my organization via the Leave Organization button on the Organization Details page. I also want to be able to see my org's member only events on the right side of the Organization Details page (Member Mark organization Details Page).

As **Member Mark**, I want to be able to view my organization's roster the same way **Sally Student** does.

As **Member Mark**, I want to be able to view the organizations that I am a part of on my profile page as a list of clickable buttons (Member Profile Page).

### Larry Leader

As **Larry Leader**, I want to be able to be able to view all pending applicants for my organization via the View Pending Applications button on the Organization Details page. This button will take me to a list of applications that I can accept and reject via their respective buttons (Pending Applications Page).

As **Larry Leader**, I want to be able to edit my organization details via the "Edit Organization" button on the Organization Details page. This button will take me to a pre-existing edit organization page (Larry Leader organization Details).

As **Larry Leader**, I want to be able to view all members from the Roster Page/More Info page, edit their roles and titles from the Edit Member Form, and remove them from the organization from the Edit Member Form via their respective buttons on each page (Roster Page, Roster Page/More Info, and Edit Member Form).

### Rhonda Root

As **Rhonda Root**, I want to be able to do anything any persona can do but for every organization in the organization model.

## Technical Implementation Opportunities and Planning

**Existing Codebase**

- ### Dependencies
  - Users: We will need to connect users to a user object to see what organizations they are involved with.
  - Roles: The functionality will differ between roles. For instance, a student should only see member-only information for the organizations that they are a part of. However, the root should be able to see all information on the site. Meanwhile, the leaders of a certain organization should be able to see all information pertaining to their organization.
    - Of course, this means we will rely on the current authentification system to know who can access and modify certain data.
- ### Extensions
  - We need to create entirely new database tables and schemas to store the organization information, but they will need to be on top of the existing database tables like users and organizations.
    - **Members** Table that relates **users** with **orgs** and adds a role attribute.
    - Table that relates organizations to their member-only information/events feed (may need to be two separate tables).
    - **Applications** Table that holds all pending applications for all organizations and relates **users** with **orgs**.
  - We will need to add or extend several frontend components to accomodate for the new pages seen in the wireframes (member lists, organization pages, forms, etc.).
- ### **Page Components and Widgets**
  - Organization Details Component: We will have to modify the currently existing organization component to display more data shown in our wireframe. There will a button to either join, request to join, view pending applications, edit the organization, or leave the club based on respective personas. There will also be text that shows if the club is closed in this component.
    - Organization Leading Roles: Adding a new mat-card to the Organization Details Component to display the names and the roles of current leaders of the organization. This section will also have a button that routes to the organization's Roster Component.
  - Organization Application Component: A form that will be filled out by students trying to apply to application-only organizations.
  - Members Only Organization Events Widget: Create a new widget that displays a list of member only events on the Organization Details Component that is only viewable by a member or leader.
  - Roster Component: A page that will list all of the members for a given organization for members/admins to view. Will display a table displaying all members of an organization with drop-down menus to show more information. This table will also include an edit button for each member (row) that only leaders will be able to see.
  - Edit Member Component: Create a new component that allows for leaders to assign a position to any student on their roster, remove a member from their organization, or give them leader privileges.
  - Pending Applicants Component: Page that will list all students that have submitted a request to join form. These will be displayed in a very similar way to the mat-table in the Roster Component. Each row will store a different applicant and there will be a drop down that displays all of the info they provided in their application. Instead of an edit button for every member, there will be an accept and reject button for every applicant.
  - Event Editor Component: Make use of the "public" attribute in the Event Entity to allow for an event to be marked members only in the form.
  - Profile Editor Component: Edit the existing profile to add a "Your Orgs" list in the form of clickable buttons that take you to that organization's details page. Also, create a "public profile" form that allows members to alter the information shown on the organization roster page.
- ### **Models**
  - Organization: We will add a type attribute to the organization model to let leaders declare the type of organization they are (open, closed, application-based).
  - Member: Model used to store a user, an organization, the user's position and leadership in the organization, and some public information the user will be able to alter.
  - Organization Applicant: Model used to store metadata from a user's application to a given organization. It will also store the user and the organization.
  - Event: We will use the existing event model with the "public" field as the members' only attribute. We can edit this model as needed.
- ### **API / Routes**
  - Get All Organizations (/organizations): Returns the current available organization model. Intended purpose is to inform users what organizations are available/unavailable. Used by all personas.
  - Get Organization (/organizations/{slug}): Returns the current organization model. Intended purpose is to display a given available organization. Used by all personas.
  - Post Applicant (/applicants/{slug}): Receives user information after appliyng to an organization. Intended purpose is to post a request for the users to apply to an organization.
  - Get All Members of an Organization (/members/{slug}): Returns all members for the given organization. Intended purpose is to display the name and info for each member in the organization. Used by all personas.
  - Get All Members of an Organization by Term (/members/{slug}/{term}): Returns all members for the given organization based on a term. Intended purpose is to display the name and info for each member in the organization for a given term. Used by all personas.
  - Get Member by ID (/members/id/id/{id}): Returns a member model. Intended to be used on the edit member page. Used by leaders and root.
  - Delete Member (/members/{slug}/members/{user_id}): Removes the member from the organization.
  - Post Member (/members/{slug}/create/{user_id}/{term}): Accepts the student's application and adds them to the organization, or allows a student to add themselves to an organization if it is open.
  - Delete Applicant (/applicants/{id}): Rejects the student's application and deletes their application from the database.
  - Put Member (/members): Updates the member model.
- ### **Security and Privacy concerns**
  - Only members of an organization should be able to see member-only information and events.
  - Only **Rhonda Root** and **Larry Leader** will be add and remove members from organizations and edit the organization's details.
  - Only **Rhonda Root** will be able to add or delete organizations.
