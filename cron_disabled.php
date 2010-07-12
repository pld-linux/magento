<?
if (!$_SERVER["HTTP_USER_AGENT"]) { // to run via local browser use if ($_SERVER["SERVER_ADDR"] == $_SERVER["REMOTE_ADDR"]) {
  setlocale(LC_ALL, 'it_IT');
  $profileId = 9; // SYSTEM - IMPORT/EXPORT - ADVANCED PROFILES
  $storeId = 1; // used when create grouped products only
  $websiteId = 1; // used when create grouped products only

  require_once 'app/Mage.php';
  umask(0);
  Mage::app("default")->setCurrentStore(Mage_Core_Model_App::ADMIN_STORE_ID);
  $profile = Mage::getModel('dataflow/profile');
  $userModel = Mage::getModel('admin/user');
  $userModel->setUserId(0);
  Mage::getSingleton('admin/session')->setUser($userModel);
  $profile->load($profileId);
  if (!$profile->getId()) {
    Mage::getSingleton('adminhtml/session')->addError('ERROR: Incorrect profile id');
  }
  Mage::register('current_convert_profile', $profile);
  $profile->run();
  
  $recordCount = 0;
  $batchModel = Mage::getSingleton('dataflow/batch');
  if ($batchModel->getId()) {
    if ($batchModel->getAdapter()) {
      $batchId = $batchModel->getId();
      $batchImportModel = $batchModel->getBatchImportModel();
      $importIds = $batchImportModel->getIdCollection();  
      $batchModel = Mage::getModel('dataflow/batch')->load($batchId);      
      $adapter = Mage::getModel($batchModel->getAdapter());
      $resource = Mage::getSingleton('core/resource');
      $product_table = $resource->getTableName('catalog/product');
      $attribute_table = $resource->getTableName('eav/attribute');
      $super_link_table = $resource->getTableName('catalog/product_super_link');
      $super_attribute_table = $resource->getTableName('catalog/product_super_attribute');
      $product_link_table = $resource->getTableName('catalog/product_link');
      $product_link_attribute_decimal_table = $resource->getTableName('catalog/product_link_attribute_decimal');
      $product_link_attribute_int_table = $resource->getTableName('catalog/product_link_attribute_int');
      $index_eav_table = $resource->getTableName('catalogindex_eav');
      $index_minimal_price_table = $resource->getTableName('catalogindex_minimal_price');
      $index_price_table = $resource->getTableName('catalogindex_price');
      // $search_fulltext_table = $resource->getTableName('catalogsearch_fulltext');
      $customer_group_table = $resource->getTableName('customer_group');
      $write = $resource->getConnection('catalog_write');
      foreach ($profile->getExceptions() as $e) {
        printf($e->getMessage() . "\n");
      }
      $exceptionCount = count($profile->getExceptions());
      foreach ($importIds as $importId) {
        $recordCount++;
        try{
          $batchImportModel->load($importId);
          if (!$batchImportModel->getId()) {
             $errors[] = Mage::helper('dataflow')->__('WARNING: Skip undefined row');
             continue;
          }
          $importData = $batchImportModel->getBatchData();
          try {
            $adapter->saveRow($importData);
	    if ($importData['type'] == 'configurable') { // for configurable products
	      $parent_id = $write->fetchOne("select * from $product_table where sku='".$importData['sku']."'");
	      $attribute_id = $write->fetchOne("select * from $attribute_table where attribute_code='".$importData['config_attributes']."'");
	      if (!$write->fetchOne("select * from $super_attribute_table where product_id=".(int)$parent_id." and attribute_id=".(int)$attribute_id)) {
	        $write->query("insert into $super_attribute_table (product_id, attribute_id) values (".(int)$parent_id.", ".(int)$attribute_id.")");
	      }
	      foreach (explode(',', $importData['associated']) as $product_sku) {
		try {
	          $product_id = $write->fetchOne("select * from $product_table where sku='$product_sku'");
		  if (!$write->fetchOne("select * from $super_link_table where parent_id=".(int)$parent_id." and product_id=".(int)$product_id)) {
		    $write->query("insert into $super_link_table (parent_id, product_id) values (".(int)$parent_id.", ".(int)$product_id.")");
		  }
		} catch (Exception $e) {
                  printf("ROW " . $recordCount . ", PARENT SKU " . $importData['sku'] . ", PRODUCT SKU " . $product_sku . " - " . $e->getMessage() . "\n");
	 	}
	      }
	    }
	    if ($importData['type'] == 'grouped') { // for grouped products
	      $parent_id = $write->fetchOne("select * from $product_table where sku='".$importData['sku']."'");
	      $valueCount = 1;
	      foreach (explode(',', $importData['associated']) as $product_sku) {
		try {
	          $product_id = $write->fetchOne("select * from $product_table where sku='$product_sku'");
		} catch (Exception $e) {
                  printf("ROW " . $recordCount . ", PARENT SKU " . $importData['sku'] . ", PRODUCT SKU " . $product_sku . " - " . $e->getMessage() . "\n");
	 	  continue;
	        }
		try {
		  if (!$write->fetchOne("select * from $product_link_table where product_id=".(int)$parent_id." and linked_product_id=".(int)$product_id." and link_type_id=3")) {
		    $write->query("insert into $product_link_table (product_id, linked_product_id, link_type_id) values (".(int)$parent_id.", ".(int)$product_id.",3)");
		  }
		  $link_id = $write->fetchOne("select link_id from $product_link_table where product_id=".(int)$parent_id." and linked_product_id=".(int)$product_id." and link_type_id=3");
		  if (!$write->fetchOne("select * from $product_link_attribute_decimal_table where product_link_attribute_id=8 and link_id=".(int)$link_id)) {
		    $write->query("insert into $product_link_attribute_decimal_table (product_link_attribute_id, link_id) values (8, ".(int)$link_id.")");
		  }
		  if (!$write->fetchOne("select * from $product_link_attribute_int_table where product_link_attribute_id=7 and link_id=".(int)$link_id)) {
		    $write->query("insert into $product_link_attribute_int_table (product_link_attribute_id, link_id) values (7, ".(int)$link_id.")");
		  }
		  $attribute_id = $write->fetchOne("select * from $attribute_table where attribute_code='".$importData['config_attributes']."'");
		  if (!$write->fetchOne("select * from $index_eav_table where store_id=".$storeId." and entity_id=".(int)$parent_id." and attribute_id=".(int)$attribute_id)) {
		    $write->query("insert into $index_eav_table (store_id, entity_id, attribute_id, value) values (".$storeId.", ".(int)$parent_id.", ".$attribute_id.", ".$valueCount++.")");
		  }
		  $customer_groups = $write->query("select customer_group_id from $customer_group_table");
		  $price_attribute = 60;
		  foreach ($customer_groups as $customer_group_id) {
		    if (!$write->fetchOne("select * from $index_minimal_price_table where entity_id=".(int)$parent_id." and customer_group_id=".(int)$customer_group_id['customer_group_id']." and website_id=".$websiteId)) {
		      $write->query("insert into $index_minimal_price_table (entity_id, customer_group_id, website_id) values (".(int)$parent_id.", ".(int)$customer_group_id['customer_group_id'].", ".$websiteId.")");
		    }
		    if (!$write->fetchOne("select * from $index_price_table where entity_id=".(int)$parent_id." and attribute_id=".$price_attribute." and customer_group_id=".(int)$customer_group_id['customer_group_id']." and website_id=".$websiteId)) {
		      $write->query("insert into $index_price_table (entity_id, attribute_id, customer_group_id, value, website_id) values (".(int)$parent_id.", ".$price_attribute.", ".(int)$customer_group_id['customer_group_id'].", ".(int)$importData['price'].", ".$websiteId.")");
		    }
		  }
		} catch (Exception $e) {
                  printf("ROW " . $recordCount . ", PARENT SKU " . $importData['sku'] . ", PRODUCT SKU " . $product_sku . " - " . $e->getMessage() . "\n");
	 	}
	      }
	    }
          } catch (Exception $e) {
            printf("ROW " . $recordCount . ", SKU " . $importData['sku'] . " - " . $e->getMessage() . "\n");
	    continue;
          }
          if ($recordCount%100 == 0) {
            printf($recordCount . "...\n");          
          }
        } catch(Exception $ex) {
          printf("ROW " . $recordCount . ", SKU " . $importData['sku'] . " - " . $e->getMessage() . "\n");          
        }
      }
      foreach ($profile->getExceptions() as $e) {
	$exceptionCount>0 ? $exceptionCount-- : printf($e->getMessage() . "\n");
      }
    }
    printf("Done\n");
  }
}
?>
