#include <pcl/PCLPointCloud2.h>
#include <pcl/io/pcd_io.h>
#include <pcl/features/fpfh.h>
#include <pcl/console/print.h>
#include <pcl/console/parse.h>
#include <pcl/console/time.h>
#include <pcl/common/transforms.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/point_types.h>

using namespace pcl;
using namespace pcl::io;
using namespace pcl::console;

Eigen::Vector4f    translation;
Eigen::Quaternionf orientation;

bool loadCloud (const std::string &filename, pcl::PCLPointCloud2 &cloud){
  TicToc tt;
  print_highlight ("Loading "); print_value ("%s ", filename.c_str ());

  tt.tic ();
  if (loadPCDFile (filename, cloud, translation, orientation) < 0)
    return (false);
  print_info ("[done, "); print_value ("%g", tt.toc ()); print_info (" ms : "); print_value ("%d", cloud.width * cloud.height); print_info (" points]\n");
  print_info ("Available dimensions: "); print_value ("%s\n", getFieldsList (cloud).c_str ());

  return (true);
}

void transform (const pcl::PCLPointCloud2::ConstPtr &input, pcl::PCLPointCloud2 &output) {
  // Check for 'normals'
  bool has_normals = false;
  for (size_t i = 0; i < input->fields.size (); ++i)
    if (input->fields[i].name == "normals")
      has_normals = true;

  // Estimate
  TicToc tt;
  tt.tic ();
  print_highlight (stderr, "Transforming ");

  // Convert data to PointCloud<T>
  if (has_normals)
  {
    PointCloud<PointNormal> xyznormals;
    fromPCLPointCloud2 (*input, xyznormals);
    pcl::transformPointCloud<PointNormal> (xyznormals, xyznormals, translation.head<3> (), orientation);
    // Copy back the xyz and normals
    pcl::PCLPointCloud2 output_xyznormals;
    toPCLPointCloud2 (xyznormals, output_xyznormals);
    concatenateFields (*input, output_xyznormals, output);
  }
  else
  {
    PointCloud<PointXYZ> xyz;
    fromPCLPointCloud2 (*input, xyz);
    pcl::transformPointCloud<PointXYZ> (xyz, xyz, translation.head<3> (), orientation);
    // Copy back the xyz and normals
    pcl::PCLPointCloud2 output_xyz;
    toPCLPointCloud2 (xyz, output_xyz);
    concatenateFields (*input, output_xyz, output);
  }

  translation = Eigen::Vector4f::Zero ();
  orientation = Eigen::Quaternionf::Identity ();

  print_info ("[done, "); print_value ("%g", tt.toc ()); print_info (" ms : "); print_value ("%d", output.width * output.height); print_info (" points]\n");
}

void saveCloud (const std::string &filename, const pcl::PCLPointCloud2 &output){
  TicToc tt;
  tt.tic ();

  print_highlight ("Saving "); print_value ("%s ", filename.c_str ());
  
  PCDWriter writer;
  writer.writeASCII(filename, output, translation, orientation);
  
  print_info ("[done, "); print_value ("%g", tt.toc ()); print_info (" ms : "); print_value ("%d", output.width * output.height); print_info (" points]\n");
}

/* ---[ */
int main (int argc, char** argv){
  // Parse the command line arguments for .pcd files
  std::vector<int> p_file_indices;
  p_file_indices = parse_file_extension_argument (argc, argv, ".pcd");
  if (p_file_indices.size () != 2)
  {
    print_error ("Need one input PCD file and one output PCD file to continue.\n");
    return (-1);
  }

  // Load the first file
  pcl::PCLPointCloud2::Ptr cloud (new pcl::PCLPointCloud2);
  if (!loadCloud (argv[p_file_indices[0]], *cloud)) 
    return (-1);

  // Perform the feature estimation
  pcl::PCLPointCloud2 output;
  transform (cloud, output);

  // Create the filtering object
  pcl::VoxelGrid<pcl::PCLPointCloud2> sor;
  sor.setInputCloud (cloud);
  sor.setLeafSize (0.01f, 0.01f, 0.01f);
  //sor.filter (*cloud_filtered);

  // Save into the second file
  saveCloud (argv[p_file_indices[1]], output);

 return 0;
}

