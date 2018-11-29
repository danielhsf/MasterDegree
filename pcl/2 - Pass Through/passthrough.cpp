#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/PCLPointCloud2.h>
#include <pcl/conversions.h>

int main (int argc, char** argv)
{
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);
  

  // Fill in the cloud data
  pcl::PCDReader reader;
  // Replace the path below with the path where you saved your file
  reader.read ("novo.pcd", *cloud); // Remember to download the file first!

  // Create the filtering object
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud (cloud);
  pass.setFilterFieldName ("y");
  pass.setFilterLimits (0, 1.2);
  //pass.setFilterLimitsNegative (true);
  pass.filter (*cloud_filtered);
  
  pass.setInputCloud (cloud_filtered);
  pass.setFilterFieldName ("x");
  pass.setFilterLimits (-0.30, 0.3);
  //pass.setFilterLimitsNegative (true);
  pass.filter (*cloud_filtered);
  
  pcl::PCLPointCloud2 point_cloud2;
   pcl::toPCLPointCloud2(*cloud_filtered, point_cloud2);
  pcl::PCDWriter writer;
  Eigen::Vector4f    translation;
  Eigen::Quaternionf orientation;
  translation = Eigen::Vector4f::Zero ();
  orientation = Eigen::Quaternionf::Identity ();
  writer.writeASCII("2-novo.pcd", point_cloud2, translation, orientation);

  std::cerr << "Cloud after filtering: " << std::endl;
  for (size_t i = 0; i < cloud_filtered->points.size (); ++i)
    std::cerr << "    " << cloud_filtered->points[i].x << " " 
                        << cloud_filtered->points[i].y << " " 
                        << cloud_filtered->points[i].z << std::endl;


  return (0);
}
