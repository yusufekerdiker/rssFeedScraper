// export interface News {
//   CNET: Article[];
//   Wired: Article[];
// }

// export interface Article {
//   articleImg: string;
//   categories: string[];
//   creator: string;
//   description: string;
//   link: string;
//   publishDate: string;
//   title: string;
// }

export interface News {
  [publisher: string]: Article[];
}

export interface Article {
  articleImg: string;
  categories: string[];
  creator: string;
  description: string;
  link: string;
  publishDate: string;
  title: string;
}
