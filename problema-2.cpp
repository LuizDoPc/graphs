#include <iostream>
#include <vector>
using namespace std;

int main(void){
    int n;
    cin >> n;
    string locais[n];
    for(int i=0; i<n; i++){
        cin >> locais[i];
    }
    int v;
    cin >> v;
    int adj[n][n];

    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            adj[i][j] = 0;
        }
    }

    for(int i=0; i<v; i++){
        string l1, l2;
        cin >> l1 >> l2;

        int linha, coluna;
        for(int j=0; j<n; j++){
            if(locais[j] == l1){
                 linha = j;
            }
            if(locais[j] == l2){
                coluna = j;
            }
        }
        adj[linha][coluna] = 1;
        adj[coluna][linha] = 1;
    }

    cout << endl;

    // for(int i=0; i<n; i++){
    //     for(int j=0; j<n; j++){
    //         cout << adj[i][j] << " ";
    //     }
    //     cout << endl;
    // }

    vector<int> cameras;
    int teste[n][3];

    int cont = 0;
    for(int k = 0;k < n;k++)
        for(int i = 0;i < n;i++)
            for(int j = 0;j < n;j++){
                if(adj[i][j] == 0 and adj[i][k] == 1 and adj[k][j] == 1 ) {
                    teste[cont][0] = i;
                    teste[cont][1] = j;
                    teste[cont][2] = k;
                    cont++;
                }
            }
    for(int i = 0; i< n;i++){
       for(int j=0; j< 3;j++){
            cout << teste[i][j] << " ";
        }
        cout << endl;
    }
    // for(int i=0; i<(int)cameras.size(); i++){
    //     cout << locais[cameras[i]] << endl;
    // }

}


// 6
// pao-de-acucar
// maracana
// copacabana
// ipanema
// corcovado
// lapa
// 7
// ipanema copacabana
// copacabana pao-de-acucar
// ipanema pao-de-acucar
// maracana lapa
// pao-de-acucar maracana
// corcovado pao-de-acucar
// lapa corcovado

// 5
// baia-de-guanabara
// centro
// jardim-botanico
// confeitaria-colombo
// sambodromo
// 4
// baia-de-guanabara sambodromo
// centro sambodromo
// sambodromo jardim-botanico
// confeitaria-colombo sambodromo