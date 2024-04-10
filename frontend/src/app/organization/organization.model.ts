/**
 * The Organization Model defines the shape of Organization data
 * retrieved from the Organization Service and the API.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Event } from '../event/event.model';
import { Profile } from '../models.module';

export enum MemberYear {
  FRESHMAN = 1,
  SOPHOMORE = 2,
  JUNIOR = 3,
  SENIOR = 4,
  FIFTH_YEAR = 5,
  GRAD = 6
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
}

export interface Member {
  user_id: number;
  organization_id: number;
  year: MemberYear;
  description: string;
  isLeader: boolean;
  position: string;
  major: string;
  minor: string;
  user: Profile;
  organization: Organization;
}
