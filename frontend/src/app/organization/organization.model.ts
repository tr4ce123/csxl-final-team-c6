/**
 * The Organization Model defines the shape of Organization data
 * retrieved from the Organization Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { NonNullableFormBuilder } from '@angular/forms';
import { Event } from '../event/event.model';
import { Profile } from '../models.module';

export enum OrganizationType {
  OPEN = 0,
  APP = 1,
  CLOSED = 2
}

/** Interface for Organization Type (used on frontend for organization detail) */
export interface Organization {
  id: number | null;
  name: string;
  logo: string;
  short_description: string;
  long_description: string;
  website: string;
  email: string;
  instagram: string;
  linked_in: string;
  youtube: string;
  heel_life: string;
  public: boolean;
  slug: string;
  shorthand: string;
  events: Event[] | null;
  org_type: OrganizationType;
}

export interface Member {
  user_id: number;
  organization_id: number;
  year: string;
  description: string;
  isLeader: boolean;
  position: string;
  major: string;
  minor: string;
  user: Profile;
  organization: Organization;
}

export enum ApplicantStatus {
  Pending = 0,
  Accepted = 1,
  Rejected = -1
}

export interface Applicant {
  id: number;
  user_id: number;
  organization_id: number;
  status: ApplicantStatus;
  name: string;
  email: string;
  major: string;
  minor: string | null;
  year: string;
  pronouns: string;
  interest: string;
}
