#include <iostream>
#include <vector>
using namespace std;

void colore(int x, vector<int> *vizinhos, int *cor){
	cor[x] = 0;
	vector<int> fila; 
	fila.push_back(x); 	
	int pos = 0;

	while(pos < (int)fila.size()){ 
		int atual = fila[pos];
		pos++;

		for(int i = 0;i < (int)vizinhos[atual].size();i++){
			
			int v = vizinhos[atual][i];
			
			if(cor[v] == -1){ 
				cor[v] = 1 - cor[atual]; 			
				fila.push_back(v); 
			}
		}
	}
}

bool checa_bipartido(int n, vector<int> *vizinhos, int *cor){
	for(int i = 0;i < n;i++){
		if(cor[i] == -1){
			colore(i, vizinhos, cor);
		}
	}
	
	for(int i = 0;i < n;i++){
		for(int j = 0;j < (int)vizinhos[i].size();j++){

			int v = vizinhos[i][j];
			if(cor[i] == cor[v]) return false;
		}
	}
	
	return true;
}

int main(void){
    int n, v;
    cin >> n >> v;

    vector<int> vizinhos[n]; 
    int cor[n];

    for(int i = 0; i<n; i++) cor[i] = -1;

    for(int i=0; i<v; i++){
        int v1, v2;
        cin >> v1 >> v2;
        vizinhos[v1].push_back(v2);
    }
    if(checa_bipartido(n, vizinhos, cor)){
        cout << "SIM" << endl;
    }else{
        cout << "NAO" << endl;
    }
}