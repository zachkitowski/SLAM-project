/**
* This file is a modified version of ORB-SLAM2.<https://github.com/raulmur/ORB_SLAM2>
*
* This file is part of DynaSLAM.
* Copyright (C) 2018 Berta Bescos <bbescos at unizar dot es> (University of Zaragoza)
* For more information see <https://github.com/bertabescos/DynaSLAM>.
*
*/


#include<iostream>
#include<algorithm>
#include<fstream>
#include<chrono>
#include <unistd.h>
#include<opencv2/core/core.hpp>

#include "Geometry.h"
#include "MaskNet.h"
#include<System.h>

using namespace std;

// ZK
void LoadImages(const string &strImagePath, const string &strFile, vector<string> &vstrImageFilenames, vector<double> &vTimestamps);

// Theirs
// void LoadImages(const string &strFile, vector<string> &vstrImageFilenames,
//                 vector<double> &vTimestamps);

int main(int argc, char **argv)
{
    if(argc != 5 && argc != 6)
    {
        cerr << endl << "Usage: ./mono_tum path_to_vocabulary path_to_settings path_to_sequence (path_to_masks)" << endl;
        return 1;
    }

    // Retrieve paths to images
    vector<string> vstrImageFilenames;
    vector<double> vTimestamps;
    // string strFile = string(argv[3])+"/rgb.txt";
    string imagePath = string(argv[3]);
    string strFile = string(argv[4]);

    cout <<"HELLO"<<endl;
    // std::cout <<"Data file: "<<string(argv[3]) <<endl;
    std::cout <<"Data file: "<<string(argv[3]) <<endl;
    std::cout <<"Image Names list.txt:"<<string(argv[4])<<endl;

    // ZK
    LoadImages(imagePath,  strFile, vstrImageFilenames, vTimestamps);

    // Theirs
    // LoadImages(strFile, vstrImageFilenames, vTimestamps);

    int nImages = vstrImageFilenames.size();

    // Initialize Mask R-CNN
    DynaSLAM::SegmentDynObject* MaskNet;
    if (argc==6)
    {
        cout << "Loading Mask R-CNN. This could take a while..." << endl;
        MaskNet = new DynaSLAM::SegmentDynObject();
        cout << "Mask R-CNN loaded!" << endl;
    }

    // Create SLAM system. It initializes all system threads and gets ready to process frames.
    ORB_SLAM2::System SLAM(argv[1],argv[2],ORB_SLAM2::System::MONOCULAR,true);

    // Vector for tracking time statistics
    vector<float> vTimesTrack;
    vTimesTrack.resize(nImages);

    cout << endl << "-------" << endl;
    cout << "Start processing sequence ..." << endl;
    cout << "Images in the sequence: " << nImages << endl << endl;

    // Main loop
    cv::Mat im;

    // Dilation settings
    int dilation_size = 15;
    cv::Mat kernel = getStructuringElement(cv::MORPH_ELLIPSE,
                                        cv::Size( 2*dilation_size + 1, 2*dilation_size+1 ),
                                        cv::Point( dilation_size, dilation_size ) );

    for(int ni=0; ni<nImages; ni++)
    {
        // Read image from file
        // im = cv::imread(string(argv[3])+"/"+vstrImageFilenames[ni],CV_LOAD_IMAGE_UNCHANGED);
        //cout <<"Reading from:" <<string(vstrImageFilenames[ni]) <<endl;
        if(ni%100 ==0){
            cout << ni <<endl;
        }

        im = cv::imread(string(vstrImageFilenames[ni]),CV_LOAD_IMAGE_UNCHANGED);
        // cout << "Read"<<endl;
        double tframe = vTimestamps[ni];

        if(im.empty())
        {
            // cerr << endl << "Failed to load image at: "
            //      << string(argv[3]) << "/" << vstrImageFilenames[ni] << endl;
            cerr << endl << "Failed to load image at: "
                 <<  vstrImageFilenames[ni] << endl;

            return 1;
        }

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t1 = std::chrono::monotonic_clock::now();
#endif
        // cout << "Before mask:"<<endl;
        // Segment out the images
        // cv::Mat mask = cv::Mat::ones(480,640,CV_8U);

        // cout << im.rows << ","<<im.cols<<endl;
        // cv::Mat mask = cv::Mat::ones(1080,1920,CV_8U); //cam1
        // cv::Mat mask = cv::Mat::ones(720,1280,CV_8U); //cam2
        cv::Mat mask = cv::Mat::ones(720,1280,CV_8U); //cam3
        // cv::Mat mask = cv::Mat::ones(480,752,CV_8U); //euro


        if(argc == 6)
        {
        	cout <<"Using MaskRCNN"<<endl;
            cv::Mat maskRCNN;
            cout << string(argv[5]) <<endl;
            maskRCNN = MaskNet->GetSegmentation(im,string(argv[5]),vstrImageFilenames[ni].replace(0,4,"")); //0 background y 1 foreground
            cv::Mat maskRCNNdil = maskRCNN.clone();
            cv::dilate(maskRCNN,maskRCNNdil, kernel);
            mask = mask - maskRCNNdil;
        }

        // Pass the image to the SLAM system
        SLAM.TrackMonocular(im, mask, tframe);
        // cout << "after track:"<<endl;
#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t2 = std::chrono::monotonic_clock::now();
#endif

        double ttrack= std::chrono::duration_cast<std::chrono::duration<double> >(t2 - t1).count();

        vTimesTrack[ni]=ttrack;

        // Wait to load the next frame
        double T=0;
        if(ni<nImages-1)
            T = vTimestamps[ni+1]-tframe;
        else if(ni>0)
            T = tframe-vTimestamps[ni-1];

        if(ttrack<T)
            usleep((T-ttrack)*1e6);
    }

    // Stop all threads
    SLAM.Shutdown();

    // Tracking time statistics
    sort(vTimesTrack.begin(),vTimesTrack.end());
    float totaltime = 0;
    for(int ni=0; ni<nImages; ni++)
    {
        totaltime+=vTimesTrack[ni];
    }
    cout << "-------" << endl << endl;
    cout << "median tracking time: " << vTimesTrack[nImages/2] << endl;
    cout << "mean tracking time: " << totaltime/nImages << endl;

    // Save camera trajectory
    
    SLAM.SaveKeyFrameTrajectoryTUM("KeyFrameTrajectory.txt");
    cout << "wrote to KeyFrameTrajectory.txt" << endl;
    string outputFileName = string(argv[3]);
    outputFileName+="_";
    outputFileName+="KeyFrameTrajectory_DynaSLAM.txt";
    SLAM.SaveKeyFrameTrajectoryTUM(outputFileName);

    return 0;
}

// Mine
void LoadImages(const string &strImagePath, const string &strFile, vector<string> &vstrImageFilenames, vector<double> &vTimestamps)
{
    ifstream f;
    f.open(strFile.c_str());


    cout << "strImagePath:"<<strImagePath<<endl;
    cout << "strFile:"<<strFile<<endl;
    // skip first three lines
    string s0;

    while(!f.eof())
    {
        string s;
        getline(f,s);
        if(!s.empty())
        {

            stringstream ss;
            ss << s;

            vstrImageFilenames.push_back(strImagePath + "/" +"frame"+ ss.str() + ".jpg"); //ours
            // vstrImageFilenames.push_back(strImagePath + "/" + ss.str() + ".png"); // euroc

            double t;
            ss >> t;
            // std::cout <<"t:"<<t << endl;
            // vTimestamps.push_back(t/1e9);
            vTimestamps.push_back(t);


            // stringstream ss;
            // ss << s;
            // double t;
            // string sRGB;
            // ss >> t;
            // vTimestamps.push_back(t);
            // ss >> sRGB;
            // vstrImageFilenames.push_back(sRGB);
        }
    }

    cout <<"vstrImageFilenames:" << vstrImageFilenames.size()<<" "<< vstrImageFilenames[0] << endl;
    cout <<"vTimestamps:"<< vTimestamps.size() <<" "<< vTimestamps[0]<<endl;
}







// void LoadImages(const string &strFile, vector<string> &vstrImageFilenames, vector<double> &vTimestamps)
// {
//     ifstream f;
//     f.open(strFile.c_str());

//     // skip first three lines
//     string s0;
//     getline(f,s0);
//     getline(f,s0);
//     getline(f,s0);

//     while(!f.eof())
//     {
//         string s;
//         getline(f,s);
//         if(!s.empty())
//         {
//             stringstream ss;
//             ss << s;
//             double t;
//             string sRGB;
//             ss >> t;
//             vTimestamps.push_back(t);
//             ss >> sRGB;
//             vstrImageFilenames.push_back(sRGB);
//         }
//     }
// }
