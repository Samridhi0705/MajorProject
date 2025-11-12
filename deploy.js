async function main() {
  console.log("Deploying MessageHashStorage contract to Ganache...");

  // Get the contract factory
  const MessageHashStorage = await hre.ethers.getContractFactory("MessageHashStorage");
  
  // Deploy the contract
  const messageHashStorage = await MessageHashStorage.deploy();
  
  // Wait for deployment to finish
  await messageHashStorage.waitForDeployment();
  
  const address = await messageHashStorage.getAddress();
  
  console.log("\n✅ MessageHashStorage deployed successfully!");
  console.log("📍 Contract address:", address);
  console.log("\n📋 Copy this address and use it to update your files!");
  console.log("Run this command:");
  console.log(`node update_address.js ${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
