import { Pipe, PipeTransform } from '@angular/core';
import { News, Article } from '../models/news';

@Pipe({
  name: 'searchFilter'
})
export class SearchFilterPipe implements PipeTransform {

  transform(value: Article[], searchTerm: string): Article[] {
    if (!value) {
      return [];
    }
    if (!searchTerm) {
      return value;
    }
    searchTerm = searchTerm.toLocaleLowerCase();
    return value.filter((article: Article) =>
      article.title.toLocaleLowerCase().includes(searchTerm) ||
      article.description.toLocaleLowerCase().includes(searchTerm)
    );
  }

}
