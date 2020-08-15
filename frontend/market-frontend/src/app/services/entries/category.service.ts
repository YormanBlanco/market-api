import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Category } from '/home/yb/Documents/YB/Programacion/DjangoProjects/drf_api/market/frontend/market-frontend/src/app/interfaces/entries';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {

  API_ENDPOINT = 'http://localhost:8000/entries/'; //la ruta de la api

  constructor(private httpClient: HttpClient) { }
  //CRUD category
  get(){
    return this.httpClient.get(this.API_ENDPOINT + 'category/');
    
  }


}

