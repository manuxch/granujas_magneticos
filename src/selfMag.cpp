/** \mainpage selfMag
 * \brief Simulación de granos magnéticos autopropulsados.
 * 
 * Programa que implementa la biblioteca Box2D para simular un sistema
 * de granos autopropulsados con dipolos magnéticos.
 *
 * \author Manuel Carlevaro <manuel@iflysib.unlp.edu.ar>
 * \version 2.1 
 * \date 2023.04.22
 */


#include <iostream>
using namespace std;
#include <box2d/box2d.h>
#include "globalSetup.hpp"
#include <string>
#include <cmath>
using std::sin; using std::cos; using std::fabs;
#include <iomanip>
#include <sstream>
#include <cstdlib>
using std::exit;
#include "sisAux.hpp"
#include "random.hpp"

int main(int argc, char *argv[])
{
    cout << "# selfMag" << endl;
    cout << "# v2.1 [2023.04.22]" << endl;
    string inputParFile(argv[1]);
    GlobalSetup *globalSetup = new GlobalSetup(inputParFile); 
    RandomGenerator rng(globalSetup->randomSeed);
    cout << "# Creación del sistema ..." << endl;

    // Definición del mundo
    //b2Vec2 gravedad(0.0f, globalSetup->g );
    b2Vec2 gravedad(0.0f, 0.0f);
    b2World world(gravedad);
    cout << "#\t- Objeto mundo creado." << endl;
    
    // Definición del contenedor
    b2BodyDef caja_def;
    caja_def.position.Set(0.0f, 0.0f);
    caja_def.type = b2_staticBody;
    
    BodyData* cajaD = new BodyData;
    cajaD->isGrain = false;
    cajaD->nLados = globalSetup->caja.nVerts;
    cajaD->gID = -100;
    cajaD->m = 0.0f;
    cajaD->r = 0;
    caja_def.userData.pointer = uintptr_t(cajaD);

    b2Body* caja;
    caja = world.CreateBody(&caja_def);
    
    int32 nverts = globalSetup->caja.nVerts;
    float xtmp, ytmp;
    b2Vec2 *verts = new b2Vec2[nverts];
    float angle = 0.0; 
    float delta_angle = 360.0/nverts;
    for (int i = 0; i < nverts; ++i) {
        xtmp = globalSetup->caja.R * cos(angle * b2_pi / 180.0f);
        ytmp = globalSetup->caja.R * sin(angle * b2_pi / 180.0f);
        verts[i].Set(xtmp, ytmp);
        angle -= delta_angle;
    }
    b2ChainShape cajaShape;
    cajaShape.CreateLoop(verts, nverts);
    b2FixtureDef cajaFix;
    cajaFix.shape = &cajaShape;
    cajaFix.density = 0.0f;
    cajaFix.friction = globalSetup->caja.fric;
    caja->CreateFixture(&cajaFix);
    float areaCaja = 0.5 * nverts * globalSetup->caja.R * globalSetup->caja.R
         * sin(2.0 * b2_pi / nverts);
    cout << "#\t- Caja creada con area " << areaCaja << " m^2." << endl;
    
    // Generación de granos.
    float xInf, xSup, yInf, ySup, x, y;
    float mg = 0.0;
    int noTotGranos = 0;
    xInf = 0.707107f * globalSetup->caja.R; // srtq(2) * R
    xSup = -0.707107f * globalSetup->caja.R;
    yInf = 0.707107f * globalSetup->caja.R;
    ySup = -0.707107f * globalSetup->caja.R;

    BodyData **gInfo;
    gInfo = new BodyData*[globalSetup->noTipoGranos];
    float areaGranos = 0.0;
    
    int contGid = 1;
    for (int i = 0; i < globalSetup->noTipoGranos; i++) { /* Loop sobre tipos 
                                                             de granos. */
        gInfo[i] = new BodyData[globalSetup->granos[i]->noGranos];
        for (int j = 0; j < globalSetup->granos[i]->noGranos; j++) { /* Loop 
                                    sobre el número de granos de cada tipo.*/
            x = rng.getAB(xInf, xSup);
            y = rng.getAB(yInf, ySup);
            gInfo[i][j].tipo = i;
            gInfo[i][j].isGrain = true;
            gInfo[i][j].isMag = 
                (abs(globalSetup->granos[i]->m) > 1.0E-8 ? true : false);
            gInfo[i][j].m = globalSetup->granos[i]->m;
            gInfo[i][j].r = globalSetup->granos[i]->r;
            gInfo[i][j].nLados = globalSetup->granos[i]->nLados;
            gInfo[i][j].f.Set(0.0f, 0.0f);
            gInfo[i][j].gID = contGid++;
            b2BodyDef bd;
            bd.type = b2_dynamicBody;
            bd.allowSleep = true;
            bd.bullet = globalSetup->isBullet;
            bd.position.Set(x,y);
            bd.angle = rng.getAB(-b2_pi,b2_pi);
            bd.userData.pointer = uintptr_t(&gInfo[i][j]);
            b2Body* grain = world.CreateBody(&bd);
            // grain->SetUserData(&gInfo[i][j]);
            if (globalSetup->granos[i]->nLados == 1) {
                b2CircleShape circle;
                circle.m_radius = globalSetup->granos[i]->radio;
               //if (circle.m_radius > maxDiam) maxDiam = circle.m_radius;
                b2FixtureDef fixDef;
                fixDef.shape = &circle;
                fixDef.density = globalSetup->granos[i]->dens;
                fixDef.friction = globalSetup->granos[i]->fric;
                fixDef.restitution = globalSetup->granos[i]->rest;
                grain->CreateFixture(&fixDef);
                mg += grain->GetMass();
                areaGranos += grain->GetMass() / fixDef.density;
                if (j == 0) cout << "#\t- Grano de tipo " << i 
                    << " creado con masa " << grain->GetMass() 
                        << " kg." << endl;
            }
            else {
                b2PolygonShape poly;
                int32 vertexCount = globalSetup->granos[i]->nLados;
                b2Vec2 vertices[8];
                for (int k = 0; k < globalSetup->granos[i]->nLados; k++) 
                    vertices[k].Set(globalSetup->granos[i]->vertices[k][0],
                            globalSetup->granos[i]->vertices[k][1]);
                poly.Set(vertices,vertexCount);
                b2FixtureDef fixDef;
                fixDef.shape = &poly;
                fixDef.density = globalSetup->granos[i]->dens;
                fixDef.friction = globalSetup->granos[i]->fric;
                fixDef.restitution = globalSetup->granos[i]->rest;
                grain->CreateFixture(&fixDef);
                mg += grain->GetMass();
                areaGranos += grain->GetMass() / fixDef.density;
                if (j == 0) cout << "#\t- Grano de tipo " << i 
                    << " creado con masa " << grain->GetMass() 
                        << " kg." << endl;
            }
            noTotGranos++;
        } // Fin loop sobre el número de granos de cada tipo.
    } // Fin loop sobre tipo de granos	
    cout << "#\t- Número total de granos = " << noTotGranos << endl;
    cout << "#\t- Masa total de granos = " << mg << " kg."<< endl;
    cout << "#\t- Packing fraction obtenido = " << areaGranos / areaCaja 
        << endl;

    // Preparamos los parámetros de la simulación. 
    float timeStep = globalSetup->tStep;
    float timeS = 0.0;
    int nTap = 1;
    int32 pIterations = globalSetup->pIter;
    int32 vIterations = globalSetup->vIter;
    Energias eKU {0.0, 0.0};

    cout << "# Inicio de la simulación..." << endl;
    int paso = 0;
    bool saveFrm = (globalSetup->saveFrameFreq > 0 ? true : false);
    bool saveXVC = (globalSetup->xvcFreq > 0 ? true : false);
    bool saveEner = (globalSetup->enerFreq > 0 ? true : false);
    std::ofstream fileXVC;
    std::ofstream fileE;
    if (saveEner) {
        fileE.open(globalSetup->enerFile.c_str());
        fileE << "# t e_Kinetic e_Potential" << endl;
    }


    // Primeros pasos para satisfacer restricciones
    for (int i = 0; i < 10; ++i) world.Step(timeStep, pIterations, vIterations);
    
    // Guardo configuración inicial
    if (saveFrm) {
        saveFrame(&world, globalSetup, paso);
        //cout << "Frame " << paso << " guardado en " << timeS << endl;
    }
    // Tap inicial
    if (globalSetup->tapping) {
        apply_tap(&world, globalSetup, &rng);
    }
    bool runSim = true;
    while (runSim) {
        if (globalSetup->tapping) {
            eKU = energyCalculation(&world);
            if (eKU.eKin < globalSetup->EkStop) {
            // if (eKU.eKin / noTotGranos < globalSetup->EkStop) {
                // Guardo alguna info
                saveXVCFile(&world, globalSetup, nTap, false);
                nTap++;
                apply_tap(&world, globalSetup, &rng);
            }
        }
        // Si es necesario, aplicación de impulsos
        if (globalSetup->noiseFreq && !globalSetup->tapping && (timeS < globalSetup->tNoiseOff) 
                && !(paso % globalSetup->noiseFreq)) {
            apply_tap(&world, globalSetup, &rng);
        }

        // Cálculo y aplicación de fuerzas magnéticas y fricción con la base
        setMagneticForces(&world);
        apply_MF_base_friction(&world, globalSetup);
        
        // Guardo energías si corresponde
        if (saveEner && !(paso % globalSetup->enerFreq)) {
            eKU = energyCalculation(&world);
            fileE << timeS << " "
                  << eKU.eKin << " "
                  << eKU.ePot << endl;
        }

        // Si es necesario, guardo el frame para graficar
        if (saveFrm && !(paso % globalSetup->saveFrameFreq)) {
            saveFrame(&world, globalSetup, paso);
            //cout << "Frame " << paso << " guardado en " << timeS << endl;
        }
        // Si es necesario, guardo las coordenadas, velocidades y contactos
        if (saveXVC && !(paso % globalSetup->xvcFreq)) {
            saveXVCFile(&world, globalSetup, paso, false);
        }

        // Avance del sistema en el tiempo
        world.Step(timeStep,pIterations,vIterations);
        paso++;
        timeS += timeStep;
        runSim = end_condition(globalSetup, timeS, nTap);

        // if (timeS > globalSetup->tMax) {
            // cout << "# Máximo tiempo de simulación alcanzado." << endl;
            // runSim = false;
        // }
        // if (timeS > 0.1 * globalSetup->tMax &&
                // eKU.eKin < globalSetup->EkStop ) {
            // cout << "# Energía cinética mínima alcanzada." << endl;
            // runSim = false;
        // }
    }
    string foutName = globalSetup->finXVCFile;
    saveXVCFile(&world, globalSetup, 0, true);
    cout << "Simulación finalizada." << endl;

    
    // Clean up
    delete globalSetup;
    delete [] gInfo;
    delete [] verts;
    if (saveEner) {
        fileE.close();
    }

    return 0;
}	

