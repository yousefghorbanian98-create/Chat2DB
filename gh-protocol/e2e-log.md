## gh-protocol E2E log — 2026-10-25T10:11:40Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T10:10:12Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 10:06 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 10:10 .
drwxr-xr-x 3 runner runner 4096 Oct 25 10:10 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 10:10 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 10:10 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
ERROR        | Unable to connect to adb daemon on port: 5037
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2869
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7ff97d601000 as it is in the protected range from 0x7ff87d600000 to 0x7ff97d800000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 31792 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
INFO         | Wait for emulator (pid 2869) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:40799 is gone due to Stream removed (CANCELLED)

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792922857146.json

BUILD SUCCESSFUL in 2m 12s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2669)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tunnel up after ~4s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
tapped VPN consent at: 894 1519 (iter vpn-1)
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::542e:f471:8955:ba71/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.4): 56(84) bytes.

--- 140.82.114.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-25 10:11:23.683  2669  2669 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:11:24.116  2669  2669 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:11:24.157  2669  2669 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:11:24.329  2669  2669 D GhDiag  : connect: core.start=true 
10-25 10:11:30.761  2669  2669 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:11:31.064  2669  2669 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@1511039} — relay loop started
10-25 10:11:31.287  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.291  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.349  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.625  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=60
10-25 10:11:31.645  2669  4296 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
10-25 10:11:31.645  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=40
10-25 10:11:31.646  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=557
10-25 10:11:31.653  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=161
10-25 10:11:31.676  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=69
10-25 10:11:31.705  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 10:11:32.027  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=63
10-25 10:11:32.173  2669  4307 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:32.287  2669  4312 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:11:32.800  2669  4269 D GhDiag  : relay dns -> 178B ok
10-25 10:11:32.801  2669  4266 D GhDiag  : relay dns -> 274B ok
10-25 10:11:32.840  2669  4272 D GhDiag  : relay dns -> 269B ok
10-25 10:11:32.841  2669  4273 D GhDiag  : relay dns -> 173B ok
10-25 10:11:33.567  2669  4304 D GhDiag  : relay dns -> 160B ok
10-25 10:11:33.567  2669  4305 D GhDiag  : relay dns -> 256B ok
10-25 10:11:33.574  2669  4492 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:33.578  2669  4303 D GhDiag  : relay dns -> 260B ok
10-25 10:11:33.579  2669  4302 D GhDiag  : relay dns -> 164B ok
10-25 10:11:33.901  2669  4511 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.120  2669  4516 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.595  2669  4447 D GhDiag  : relay dns -> 160B ok
10-25 10:11:34.605  2669  4448 D GhDiag  : relay dns -> 256B ok
10-25 10:11:35.313  2669  4509 D GhDiag  : relay dns -> 44B ok
10-25 10:11:35.314  2669  4508 D GhDiag  : relay dns -> 112B ok
10-25 10:11:35.617  2669  4517 D GhDiag  : relay dns -> 45B ok
10-25 10:11:35.623  2669  4515 D GhDiag  : relay dns -> 57B ok
10-25 10:11:35.625  2669  4533 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:35.699  2669  4534 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:35.956  2669  4535 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:37.401  2669  4568 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 10:11:23.655  2669  2669 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:11:23.683  2669  2669 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:11:24.116  2669  2669 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:11:24.157  2669  2669 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:11:24.329  2669  2669 D GhDiag  : connect: core.start=true 
10-25 10:11:30.761  2669  2669 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:11:31.064  2669  2669 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@1511039} — relay loop started
10-25 10:11:31.287  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.291  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.349  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.625  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=60
10-25 10:11:31.645  2669  4296 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
10-25 10:11:31.645  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=40
10-25 10:11:31.646  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=557
10-25 10:11:31.653  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=161
10-25 10:11:31.676  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=69
10-25 10:11:31.705  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 10:11:32.027  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=63
10-25 10:11:32.173  2669  4307 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:32.287  2669  4312 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:11:32.800  2669  4269 D GhDiag  : relay dns -> 178B ok
10-25 10:11:32.801  2669  4266 D GhDiag  : relay dns -> 274B ok
10-25 10:11:32.840  2669  4272 D GhDiag  : relay dns -> 269B ok
10-25 10:11:32.841  2669  4273 D GhDiag  : relay dns -> 173B ok
10-25 10:11:33.567  2669  4304 D GhDiag  : relay dns -> 160B ok
10-25 10:11:33.567  2669  4305 D GhDiag  : relay dns -> 256B ok
10-25 10:11:33.574  2669  4492 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:33.578  2669  4303 D GhDiag  : relay dns -> 260B ok
10-25 10:11:33.579  2669  4302 D GhDiag  : relay dns -> 164B ok
10-25 10:11:33.901  2669  4511 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.120  2669  4516 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.595  2669  4447 D GhDiag  : relay dns -> 160B ok
10-25 10:11:34.605  2669  4448 D GhDiag  : relay dns -> 256B ok
10-25 10:11:35.313  2669  4509 D GhDiag  : relay dns -> 44B ok
10-25 10:11:35.314  2669  4508 D GhDiag  : relay dns -> 112B ok
10-25 10:11:35.617  2669  4517 D GhDiag  : relay dns -> 45B ok
10-25 10:11:35.623  2669  4515 D GhDiag  : relay dns -> 57B ok
10-25 10:11:35.625  2669  4533 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:35.699  2669  4534 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:35.956  2669  4535 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:37.401  2669  4568 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
tartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:11:20.022   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{b6fd9cf com.google.android.youtube/10139} BLOCKED
10-25 10:11:20.022   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{816ff5c com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:11:20.022   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{c0f265 com.google.android.as/10125} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{b202b3a com.google.android.gm/10142} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{2ba43eb com.google.android.devicelockcontroller/10173} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{cc2b548 com.google.android.dialer/10129} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{fd34fe1 com.google.android.contacts/10154} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{855c106 com.google.android.partnersetup/10124} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{df733c7 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{6f1ddf4 com.google.android.cellbroadcastreceiver/10183} BLOCKED
10-25 10:11:20.023   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{554091d com.google.android.inputmethod.latin/10140} BLOCKED
10-25 10:11:22.193  2669  3358 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 10:11:23.304  1599  1599 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 10:11:23.462   522  1444 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 10:11:23.462   829   862 V WindowManagerShell: Transition requested: android.os.BinderProxy@288dce3 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=43531 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@22566e0} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{853d99 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:11:23.643  3499  3499 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:11:23.646  3499  3499 I AndroidRuntime: Using default boot image
10-25 10:11:23.655  2669  2669 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:11:23.656  3499  3499 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:11:23.683  2669  2669 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:11:23.807  3499  3499 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:11:23.874  1599  1599 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 10:11:23.877  1599  3563 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 10:11:23.877  1599  3563 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 10:11:23.911  3566  3566 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0
10-25 10:11:23.911  3566  3566 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0
10-25 10:11:23.911  3566  3566 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0
10-25 10:11:23.911  3566  3566 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0
10-25 10:11:24.116  2669  2669 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:11:24.157  2669  2669 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:11:24.167  1471  3313 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 10:11:24.329  2669  2669 D GhDiag  : connect: core.start=true 
10-25 10:11:24.368   522  1932 D CoreBackPreview: Window{db978b5 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@e006222, mPriority=0, mIsAnimationCallback=false}
10-25 10:11:24.721   829   862 V WindowManagerShell: onTransitionReady android.os.BinderProxy@288dce3: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b3c7ef4 u0 com.ghprotocol.app/.MainActivity)/@0xffa626e sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2985588 u0 com.ghprotocol.app/.MainActivity)/@0x6ad9d0f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:11:24.722   829   862 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b3c7ef4 u0 com.ghprotocol.app/.MainActivity)/@0xffa626e sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2985588 u0 com.ghprotocol.app/.MainActivity)/@0x6ad9d0f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:11:24.722   829   862 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b3c7ef4 u0 com.ghprotocol.app/.MainActivity)/@0xffa626e sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2985588 u0 com.ghprotocol.app/.MainActivity)/@0x6ad9d0f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:11:24.722   522   539 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s249ms
10-25 10:11:24.722   522   539 V WindowManager: Sent Transition #7 createdAt=10-25 10:11:23.458 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=43531 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{8162172 Task{41c0b21 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{726619f com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:11:24.722   522   539 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{b3c7ef4 u0 com.ghprotocol.app/.MainActivity)/@0x59fe3f9 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2985588 u0 com.ghprotocol.app/.MainActivity)/@0x7c32ac0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:11:24.765  1422  3350 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 10:11:25.238   829   862 V WindowManagerShell: Transition requested: android.os.BinderProxy@5feab59 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=44874 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@57a431e} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{cb5e7ff com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:11:25.347  3620  3620 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=54421 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 10:11:25.533   522  1444 I ImeTracker: com.ghprotocol.app:e613d0a5: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 10:11:25.533   522  1444 I ImeTracker: com.ghprotocol.app:e613d0a5: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:11:25.534  1511  1511 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:11:25.650   522  1840 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 10:11:25.651   522  1840 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 10:11:25.651   522  1840 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 10:11:25.690  2669  2680 I .ghprotocol.app: Background concurrent copying GC freed 99128(5261KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 5910KB/11MB, paused 26us,10us total 187.044ms
10-25 10:11:25.804  3499  3499 I AccessibilityNodeInfoDumper: Null child 2/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.805  3499  3499 I AccessibilityNodeInfoDumper: Null child 3/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.805  3499  3499 I AccessibilityNodeInfoDumper: Null child 4/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.805  3499  3499 I AccessibilityNodeInfoDumper: Null child 5/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.806  3499  3499 I AccessibilityNodeInfoDumper: Null child 6/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.806  3499  3499 I AccessibilityNodeInfoDumper: Null child 7/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.806  3499  3499 I AccessibilityNodeInfoDumper: Null child 8/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.807  3499  3499 I AccessibilityNodeInfoDumper: Null child 9/10, parent: android.view.accessibility.AccessibilityNodeInfo@9f46; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 231 - 1080, 2400); boundsInWindow: Rect(0, 231 - 1080, 2400); packageName: com.ghprotocol.app; className: android.widget.ScrollView; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.807  3499  3499 I AccessibilityNodeInfoDumper: Null child 1/2, parent: android.view.accessibility.AccessibilityNodeInfo@9d56; boundsInParent: Rect(0, 0 - 0, 0); boundsInScreen: Rect(0, 0 - 1080, 2400); boundsInWindow: Rect(0, 0 - 1080, 2400); packageName: com.ghprotocol.app; className: android.view.View; text: null; error: null; maxTextLength: -1; stateDescription: null; contentDescription: null; tooltipText: null; containerTitle: null; viewIdResName: null; uniqueId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; contextClickable: false; enabled: true; password: false; scrollable: false; importantForAccessibility: true; visible: true; actions: [AccessibilityAction: ACTION_ACCESSIBILITY_FOCUS - null]; isTextSelectable: false
10-25 10:11:25.820  3499  3499 D AndroidRuntime: Shutting down VM
10-25 10:11:26.616   522   539 V WindowManager: Sent Transition #8 createdAt=10-25 10:11:24.801 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=44874 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{8162172 Task{41c0b21 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{439401d com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:11:27.191   522   588 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{4b82c1b com.google.android.gm/10142} BLOCKED
10-25 10:11:27.768  3905  3905 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:11:27.771  3905  3905 I AndroidRuntime: Using default boot image
10-25 10:11:27.771  3905  3905 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:11:27.870  3905  3905 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:11:28.955  3905  3905 D AndroidRuntime: Shutting down VM
10-25 10:11:29.400   522  1653 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{23d6bbb com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:11:29.401   522  3160 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{89c08d8 com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:11:30.252   522  1444 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 10:11:30.384   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{eb7c6d8 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:11:30.403   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{d2a541c com.android.camera2/10146} BLOCKED
10-25 10:11:30.409   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{a4e8825 com.google.android.gm/10142} BLOCKED
10-25 10:11:30.441   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{6969608 com.google.android.devicelockcontroller/10173} BLOCKED
10-25 10:11:30.444   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{20481a1 com.google.android.rkpdapp/10170} BLOCKED
10-25 10:11:30.448   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{40bcac6 com.google.android.projection.gearhead/10123} BLOCKED
10-25 10:11:30.462   522   572 I AppsFilter: interaction: PackageSetting{5209a2e com.ghprotocol.app/10192} -> PackageSetting{ef06fc6 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 10:11:30.756   522  2532 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 10:11:30.761  2669  2669 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:11:31.064   522  3160 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 10:11:31.064  2669  2669 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@1511039} — relay loop started
10-25 10:11:31.066   522  2348 I ImeTracker: com.ghprotocol.app:7a2bf7f1: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 10:11:31.066   522  2348 I ImeTracker: com.ghprotocol.app:7a2bf7f1: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:11:31.069  1511  1511 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:11:31.287  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.291  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.307  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 10:11:31.349  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.625  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=60
10-25 10:11:31.645  2669  4296 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
10-25 10:11:31.645  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=40
10-25 10:11:31.646  2669  4254 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=557
10-25 10:11:31.653  2669  4254 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.675  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=161
10-25 10:11:31.676  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=69
10-25 10:11:31.705  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=160
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:31.733  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 10:11:32.027  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=270
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:11:32.053  2669  4254 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=63
10-25 10:11:32.173  2669  4307 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:32.287  2669  4312 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:11:32.800  2669  4269 D GhDiag  : relay dns -> 178B ok
10-25 10:11:32.801  2669  4266 D GhDiag  : relay dns -> 274B ok
10-25 10:11:32.840  2669  4272 D GhDiag  : relay dns -> 269B ok
10-25 10:11:32.841  2669  4273 D GhDiag  : relay dns -> 173B ok
10-25 10:11:33.567  2669  4304 D GhDiag  : relay dns -> 160B ok
10-25 10:11:33.567  2669  4305 D GhDiag  : relay dns -> 256B ok
10-25 10:11:33.574  2669  4492 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:33.578  2669  4303 D GhDiag  : relay dns -> 260B ok
10-25 10:11:33.579  2669  4302 D GhDiag  : relay dns -> 164B ok
10-25 10:11:33.901  2669  4511 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.120  2669  4516 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:34.595  2669  4447 D GhDiag  : relay dns -> 160B ok
10-25 10:11:34.605  2669  4448 D GhDiag  : relay dns -> 256B ok
10-25 10:11:35.313  2669  4509 D GhDiag  : relay dns -> 44B ok
10-25 10:11:35.314  2669  4508 D GhDiag  : relay dns -> 112B ok
10-25 10:11:35.617  2669  4517 D GhDiag  : relay dns -> 45B ok
10-25 10:11:35.623  2669  4515 D GhDiag  : relay dns -> 57B ok
10-25 10:11:35.625  2669  4533 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:11:35.699  2669  4534 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:35.956  2669  4535 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:11:37.401  2669  4568 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
