## gh-protocol E2E log — 2026-10-24T16:11:51Z

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
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mapDebugSourceSetPaths
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:checkDebugAarMetadata
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:compressDebugAssets

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:64:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_2-1792857761911.json

BUILD SUCCESSFUL in 1m 52s
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
== wait for emulator external network (needed for subscription fetch) ==
emulator has network after ~4s (icmp=no validated=10)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2315)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
app died during connect flow (iter 5)
=== E2E FAILED: app process died during connect flow (logcat attached) ===


### e2e-logcat.log (crashes + app + vpn, tail)
 VM exiting with result code 0, cleanup skipped.
10-24 16:09:52.281  1117  1117 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:10:30.494   538   594 V BackupManagerService: [UserID:0] restoreAtInstall pkg=com.ghprotocol.app token=1 restoreSet=0
10-24 16:10:33.510   538   871 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10141, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-24 16:10:34.770  1910  1910 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:10:36.194   917   917 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-24 16:10:38.247   538  1495 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-24 16:10:38.346   538  1495 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 16:10:38.354   904   930 V WindowManagerShell: Transition requested: android.os.BinderProxy@dbdc901 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=334389 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@4d313a6} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{64021e7 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 16:10:38.865   538   613 D CoreBackPreview: Window{c9d7ee7 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@25b8532, mPriority=0, mIsAnimationCallback=false}
10-24 16:10:39.923   538   572 I ActivityManager: Start proc 2315:com.ghprotocol.app/u0a141 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-24 16:10:40.126   538   559 V WindowManager: Sent Transition #6 createdAt=10-24 16:10:38.074 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=334389 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c3850bc Task{4452d2a #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{9fbd845 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 16:10:40.247  2315  2315 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-24 16:10:40.270   538   559 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{c3850bc Task{4452d2a #8 type=standard A=10141:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xd9c3642 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{1eb4ccb Task{84ddb52 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x90d740b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:10:40.436  2315  2315 I .ghprotocol.app: Using CollectorTypeCC GC.
10-24 16:10:40.450  2315  2315 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-24 16:10:40.450  2315  2315 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-24 16:10:41.821  2315  2315 W ziparchive: Unable to open '/data/app/~~qoPONkr5bPpkkJWK3S8u_Q==/com.ghprotocol.app-j21VbEHudb71DhhtAPg9kg==/base.dm': No such file or directory
10-24 16:10:41.822  2315  2315 W ziparchive: Unable to open '/data/app/~~qoPONkr5bPpkkJWK3S8u_Q==/com.ghprotocol.app-j21VbEHudb71DhhtAPg9kg==/base.dm': No such file or directory
10-24 16:10:43.890   538   594 I AppsFilter: interaction: PackageSetting{3a1a2a4 com.ghprotocol.app/10141} -> PackageSetting{a38680d com.android.calendar/10100} BLOCKED
10-24 16:10:44.567  2315  2315 D nativeloader: Configuring clns-6 for other apk /data/app/~~qoPONkr5bPpkkJWK3S8u_Q==/com.ghprotocol.app-j21VbEHudb71DhhtAPg9kg==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~qoPONkr5bPpkkJWK3S8u_Q==/com.ghprotocol.app-j21VbEHudb71DhhtAPg9kg==/lib/x86_64:/data/app/~~qoPONkr5bPpkkJWK3S8u_Q==/com.ghprotocol.app-j21VbEHudb71DhhtAPg9kg==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-24 16:10:44.764  2315  2315 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-24 16:10:44.765  2315  2315 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-24 16:10:46.113   538   594 I AppsFilter: interaction: PackageSetting{3a1a2a4 com.ghprotocol.app/10141} -> PackageSetting{4e9afef com.android.camera2/10103} BLOCKED
10-24 16:10:47.923   538   594 I AppsFilter: interaction: PackageSetting{3a1a2a4 com.ghprotocol.app/10141} -> PackageSetting{eaec2de com.android.inputmethod.latin/10107} BLOCKED
10-24 16:10:49.511   904   930 V WindowManagerShell: Transition requested: android.os.BinderProxy@29a4d05 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=345554 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@608815a} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{ea4af8b com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 16:10:49.600   538  1541 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-24 16:10:49.987   538   562 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8}
10-24 16:10:50.023   538   562 W ActivityTaskManager: Activity pause timeout for ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8}
10-24 16:10:50.471   904   930 V WindowManagerShell: onTransitionReady android.os.BinderProxy@29a4d05: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity)/@0x8cd6e5f sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity)/@0x39320ac sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:10:51.887  2315  2315 W .ghprotocol.app: Verification of void androidx.compose.ui.platform.AndroidComposeView.<init>(android.content.Context, kotlin.coroutines.CoroutineContext) took 128.711ms (6666.06 bytecodes/s) (30440B approximate peak alloc)
10-24 16:10:52.039   538   559 V WindowManager: Sent Transition #7 createdAt=10-24 16:10:49.415 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=345554 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c3850bc Task{4452d2a #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=Rect(0, 128 - 0, 0) topActivityInfo=ActivityInfo{f5c7a5f com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 16:10:52.074   538   559 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity)/@0x4242468 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity)/@0xb4d7b8b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:10:55.697  2315  2315 D AndroidRuntime: Shutting down VM
10-24 16:10:55.782  2315  2315 E AndroidRuntime: FATAL EXCEPTION: main
10-24 16:10:55.782  2315  2315 E AndroidRuntime: Process: com.ghprotocol.app, PID: 2315
10-24 16:10:55.782  2315  2315 E AndroidRuntime: java.lang.RuntimeException: Cannot create an instance of class com.ghprotocol.app.ui.HomeViewModel
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider$AndroidViewModelFactory.create(ViewModelProvider.android.kt:309)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider$AndroidViewModelFactory.create(ViewModelProvider.android.kt:299)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider$AndroidViewModelFactory.create(ViewModelProvider.android.kt:273)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.SavedStateViewModelFactory.create(SavedStateViewModelFactory.kt:128)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider$Factory.create(ViewModelProvider.android.kt:158)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.ViewModelProviderImpl_androidKt.createViewModel(ViewModelProviderImpl.android.kt:34)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.ViewModelProviderImpl.getViewModel$lifecycle_viewmodel_release(ViewModelProviderImpl.kt:65)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.ViewModelProviderImpl.getViewModel$lifecycle_viewmodel_release$default(ViewModelProviderImpl.kt:47)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider.get(ViewModelProvider.android.kt:91)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.compose.ViewModelKt__ViewModelKt.get(ViewModel.kt:162)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.compose.ViewModelKt.get(Unknown Source:1)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.compose.ViewModelKt__ViewModelKt.viewModel(ViewModel.kt:103)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.viewmodel.compose.ViewModelKt.viewModel(Unknown Source:1)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at com.ghprotocol.app.ComposableSingletons$MainActivityKt$lambda-1$1.invoke(MainActivity.kt:78)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at com.ghprotocol.app.ComposableSingletons$MainActivityKt$lambda-1$1.invoke(MainActivity.kt:42)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionLocalKt.CompositionLocalProvider(CompositionLocal.kt:401)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.material3.TextKt.ProvideTextStyle(Text.kt:349)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.material3.MaterialThemeKt$MaterialTheme$1.invoke(MaterialTheme.kt:69)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.material3.MaterialThemeKt$MaterialTheme$1.invoke(MaterialTheme.kt:68)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionLocalKt.CompositionLocalProvider(CompositionLocal.kt:380)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.material3.MaterialThemeKt.MaterialTheme(MaterialTheme.kt:60)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at com.ghprotocol.app.ui.theme.ThemeKt.GhProtocolTheme(Theme.kt:39)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at com.ghprotocol.app.MainActivity$onCreate$1.invoke(MainActivity.kt:36)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at com.ghprotocol.app.MainActivity$onCreate$1.invoke(MainActivity.kt:35)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.ComposeView.Content(ComposeView.android.kt:441)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AbstractComposeView$ensureCompositionCreated$1.invoke(ComposeView.android.kt:259)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AbstractComposeView$ensureCompositionCreated$1.invoke(ComposeView.android.kt:258)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionLocalKt.CompositionLocalProvider(CompositionLocal.kt:380)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.CompositionLocalsKt.ProvideCommonCompositionLocals(CompositionLocals.kt:216)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AndroidCompositionLocals_androidKt$ProvideAndroidCompositionLocals$3.invoke(AndroidCompositionLocals.android.kt:132)
10-24 16:10:55.782  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AndroidCompositionLocals_androidKt$ProvideAndroidCompositionLocals$3.invoke(AndroidCompositionLocals.android.kt:131)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionLocalKt.CompositionLocalProvider(CompositionLocal.kt:380)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AndroidCompositionLocals_androidKt.ProvideAndroidCompositionLocals(AndroidCompositionLocals.android.kt:121)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1$1$3.invoke(Wrapper.android.kt:155)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1$1$3.invoke(Wrapper.android.kt:154)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionLocalKt.CompositionLocalProvider(CompositionLocal.kt:401)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1$1.invoke(Wrapper.android.kt:154)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1$1.invoke(Wrapper.android.kt:133)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:109)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.internal.ComposableLambdaImpl.invoke(ComposableLambda.jvm.kt:35)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.ActualJvm_jvmKt.invokeComposable(ActualJvm.jvm.kt:97)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.ComposerImpl.doCompose(Composer.kt:3595)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.ComposerImpl.composeContent$runtime_release(Composer.kt:3522)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionImpl.composeContent(Composition.kt:743)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.Recomposer.composeInitial$runtime_release(Recomposer.kt:1122)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionImpl.composeInitial(Composition.kt:649)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.runtime.CompositionImpl.setContent(Composition.kt:635)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1.invoke(Wrapper.android.kt:133)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1.invoke(Wrapper.android.kt:124)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AndroidComposeView.setOnViewTreeOwnersAvailable(AndroidComposeView.android.kt:1626)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition.setContent(Wrapper.android.kt:124)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition.onStateChanged(Wrapper.android.kt:180)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.LifecycleRegistry$ObserverWithState.dispatchEvent(LifecycleRegistry.jvm.kt:320)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.LifecycleRegistry.addObserver(LifecycleRegistry.jvm.kt:198)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1.invoke(Wrapper.android.kt:131)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.WrappedComposition$setContent$1.invoke(Wrapper.android.kt:124)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at androidx.compose.ui.platform.AndroidComposeView.onAttachedToWindow(AndroidComposeView.android.kt:1707)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.View.dispatchAttachedToWindow(View.java:21980)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewGroup.dispatchAttachedToWindow(ViewGroup.java:3490)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewGroup.dispatchAttachedToWindow(ViewGroup.java:3497)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewGroup.dispatchAttachedToWindow(ViewGroup.java:3497)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewGroup.dispatchAttachedToWindow(ViewGroup.java:3497)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewGroup.dispatchAttachedToWindow(ViewGroup.java:3497)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewRootImpl.performTraversals(ViewRootImpl.java:3014)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewRootImpl.doTraversal(ViewRootImpl.java:2465)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.ViewRootImpl$TraversalRunnable.run(ViewRootImpl.java:9305)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1339)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1348)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.Choreographer.doCallbacks(Choreographer.java:952)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.Choreographer.doFrame(Choreographer.java:882)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.view.Choreographer$FrameDisplayEventReceiver.run(Choreographer.java:1322)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.os.Handler.handleCallback(Handler.java:958)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.os.Handler.dispatchMessage(Handler.java:99)
10-24 16:10:55.853  2315  2315 E AndroidRuntime: 	at android.os.Looper.loopOnce(Looper.java:205)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at android.os.Looper.loop(Looper.java:294)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at android.app.ActivityThread.main(ActivityThread.java:8177)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at java.lang.reflect.Method.invoke(Native Method)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:552)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:971)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: Caused by: java.lang.NoSuchMethodException: com.ghprotocol.app.ui.HomeViewModel.<init> [class android.app.Application]
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at java.lang.Class.getConstructor0(Class.java:3325)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at java.lang.Class.getConstructor(Class.java:2485)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	at androidx.lifecycle.ViewModelProvider$AndroidViewModelFactory.create(ViewModelProvider.android.kt:307)
10-24 16:10:56.064  2315  2315 E AndroidRuntime: 	... 90 more
10-24 16:10:56.473   538  1541 W ActivityTaskManager:   Force finishing activity com.ghprotocol.app/.MainActivity
10-24 16:10:57.389   538  1511 I WindowManager: WIN DEATH: Window{a47f59b u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-24 16:10:57.391   538  1511 W InputManager-JNI: Input channel object 'a47f59b com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-24 16:10:57.910   538  1525 I ActivityManager: Process com.ghprotocol.app (pid 2315) has died: fg  TOP 
10-24 16:10:58.459   538  1525 W InputManager-JNI: Input channel object 'Letterbox_left_ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.525   538  1525 W InputManager-JNI: Input channel object 'Letterbox_top_ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.525   538  1525 W InputManager-JNI: Input channel object 'Letterbox_right_ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.526   538  1525 W InputManager-JNI: Input channel object 'Letterbox_bottom_ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.765   538  1525 W ActivityTaskManager: Force removing ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8}: app died, no saved state
10-24 16:10:58.767   538  1525 W InputManager-JNI: Input channel object 'Letterbox_left_ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.905   538  1525 W InputManager-JNI: Input channel object 'Letterbox_top_ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.910   538  1525 W InputManager-JNI: Input channel object 'Letterbox_right_ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:58.911   538  1525 W InputManager-JNI: Input channel object 'Letterbox_bottom_ActivityRecord{55ef9ff u0 com.ghprotocol.app/.MainActivity t8} (client)' was disposed without first being removed with the input manager!
10-24 16:10:59.321   538   562 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{59c3fd9 u0 com.ghprotocol.app/.MainActivity t-1 f}}
10-24 16:11:00.144   538   559 V WindowManager:     info={id=8 t=CLOSE f=0x10 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{c3850bc Task{4452d2a #8 type=standard A=10141:com.ghprotocol.app}}} m=CLOSE f=NONE leash=Surface(name=Task=8)/@0xd9c3642 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{1eb4ccb Task{84ddb52 #1 type=home}}} m=TO_FRONT f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x90d740b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{null m=TO_FRONT f=IS_WALLPAPER leash=Surface(name=WallpaperWindowToken{21b368a token=android.os.Binder@1fed8f5})/@0x882019a sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:11:00.487   538  1890 W InputManager-JNI: Input channel object 'c9d7ee7 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 16:11:08.348  2547  2547 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:11:08.472  2547  2547 I AndroidRuntime: Using default boot image
10-24 16:11:08.473  2547  2547 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:11:10.228   538   594 I AppsFilter: interaction: PackageSetting{3a1a2a4 com.ghprotocol.app/10141} -> PackageSetting{b0be161 com.android.rkpdapp/10129} BLOCKED
10-24 16:11:12.445  2547  2547 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:11:12.854   538   594 I AppsFilter: interaction: PackageSetting{3a1a2a4 com.ghprotocol.app/10141} -> PackageSetting{920272 com.android.rkpdapp/10129} BLOCKED
10-24 16:11:21.300  2547  2547 D AndroidRuntime: Shutting down VM
10-24 16:11:22.296  2287  2287 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.


