<?
//uncomment when moved to server - to ensure this page is not accessed from anywhere else
if (!$_SERVER["HTTP_USER_AGENT"]) {

require_once 'app/Mage.php';
// wget -O - http://<www.example.com>/Cron_Import.php
  umask(0);

  //$_SERVER['SERVER_PORT']='443';
  Mage::app();

  $profileId = 1; //put your profile id here
 
  Mage::log("Import Started",null,$logFileName);  
 
  $profile = Mage::getModel('dataflow/profile');
  
  $userModel = Mage::getModel('admin/user');
  $userModel->setUserId(0);
  Mage::getSingleton('admin/session')->setUser($userModel);
  
  if ($profileId) {
    $profile->load($profileId);
    if (!$profile->getId()) {
      Mage::getSingleton('adminhtml/session')->addError('The profile you are trying to save no longer exists');
    }
  }

  Mage::register('current_convert_profile', $profile);

  $profile->run();
  
  echo 'Export Completed';
}
?>